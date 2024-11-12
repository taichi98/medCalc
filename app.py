from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import math
import os

app = Flask(__name__)

# Hàm để đọc dữ liệu chuẩn từ các file txt
def make_standard(name):
    path = f"growthstandards/{name}.txt"
    return pd.read_csv(path, sep='\t', dtype={'sex': int, 'age': int})

# Tải các bảng dữ liệu tiêu chuẩn
growthstandards = {
    "bmi": make_standard("bmianthro"),
    "weight": make_standard("weianthro"),
    "length": make_standard("lenanthro"),
    "head": make_standard("hcanthro"),
    "wfl": make_standard("wflanthro"),
    "wfh": make_standard("wfhanthro")
}

# Hàm tính Z-score chung
def calculate_zscore(data, age, sex, measure_value):
    subset = data[(data['sex'] == sex) & (data['age'] == age)]
    if not subset.empty:
        l = subset.iloc[0]['l']
        m = subset.iloc[0]['m']
        s = subset.iloc[0]['s']
        z_score = ((measure_value / m) ** l - 1) / (s * l)
        return z_score
    else:
        return None

# Số ngày trung bình trong một tháng theo WHO
ANTHRO_DAYS_OF_MONTH = 30.4375

def round_up(x):
    if isinstance(x, (int, float)) and x >= 0:
        x_rounded = math.floor(x)
        rest = x - x_rounded
        if rest >= 0.5:
            x_rounded += 1
        return x_rounded
    elif isinstance(x, list):  
        return [round_up(val) for val in x if val >= 0]
    else:
        raise ValueError("Giá trị phải là số dương hoặc danh sách các số dương.")

def age_to_days(age, is_age_in_month):
    return int(round_up(age * ANTHRO_DAYS_OF_MONTH if is_age_in_month else age))

# Hàm điều chỉnh chiều dài/chiều cao theo tuổi và cách đo
def adjust_lenhei(age_in_days, measure, lenhei):
    age_in_days = round_up(age_in_days)
    if age_in_days < 731 and measure == "h":
        lenhei += 0.7
    elif age_in_days >= 731 and measure == "l":
        lenhei -= 0.7
    return lenhei

def calculate_zscore_weight_for_lenhei(lenhei, sex, weight, age_days=None, lenhei_unit=None):
    # Bước 1: Kiểm tra và làm sạch dữ liệu
    if weight < 0.9 or weight > 58.0:
        return None
    if lenhei < 38.0 or lenhei > 150.0:
        return None

    # Bước 2: Nội suy chiều dài/chiều cao
    low_lenhei = np.trunc(lenhei * 10) / 10
    upp_lenhei = np.trunc(lenhei * 10 + 1) / 10
    diff_lenhei = (lenhei - low_lenhei) / 0.1

    # Bước 3: Hợp nhất dữ liệu `wfl` và `wfh`
    growthstandards_wfl = growthstandards['wfl'].copy()
    growthstandards_wfh = growthstandards['wfh'].copy()
    growthstandards_wfl.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growthstandards_wfh.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growth_data = pd.concat([growthstandards_wfl, growthstandards_wfh])
    growth_data['lorh'] = growth_data['lorh'].str.lower()

    # Bước 4: Xác định chuẩn để sử dụng (wfl hoặc wfh)
    join_on_l = ((age_days is not None and age_days < 731) or
                 (age_days is None and lenhei_unit == "l") or
                 (age_days is None and lenhei_unit is None and lenhei < 87))
    join_on_h = ((age_days is not None and age_days >= 731) or
                 (age_days is None and lenhei_unit == "h") or
                 (age_days is None and lenhei_unit is None and lenhei >= 87))
    
    # Bước 5: Chọn chuẩn phù hợp từ `growth_data`
    subset_low = growth_data[(growth_data['sex'] == sex) & (growth_data['lenhei'] == low_lenhei)]
    subset_upp = growth_data[(growth_data['sex'] == sex) & (growth_data['lenhei'] == upp_lenhei)]

    # Bước 6: Nội suy m, l, s nếu có dữ liệu phù hợp ở cả low_lenhei và upp_lenhei
    if not subset_low.empty and not subset_upp.empty:
        l = subset_low.iloc[0]['l'] + diff_lenhei * (subset_upp.iloc[0]['l'] - subset_low.iloc[0]['l'])
        m = subset_low.iloc[0]['m'] + diff_lenhei * (subset_upp.iloc[0]['m'] - subset_low.iloc[0]['m'])
        s = subset_low.iloc[0]['s'] + diff_lenhei * (subset_upp.iloc[0]['s'] - subset_low.iloc[0]['s'])
    elif not subset_low.empty:
        l, m, s = subset_low.iloc[0]['l'], subset_low.iloc[0]['m'], subset_low.iloc[0]['s']
    elif not subset_upp.empty:
        l, m, s = subset_upp.iloc[0]['l'], subset_upp.iloc[0]['m'], subset_upp.iloc[0]['s']
    else:
        return None

    # Bước 7: Tính Z-score
    z_score = ((weight / m) ** l - 1) / (s * l) if l != 0 else (np.log(weight / m)) / s
    return z_score


        
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        sex = request.form.get("sex")
        age_days = int(request.form.get("ageInDays"))
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        measure = request.form.get("measure", "h").lower()
        
        # Điều chỉnh chiều dài/chiều cao
        adjusted_lenhei = adjust_lenhei(age_days, measure, height)
        
        # Tính BMI
        bmi = weight / ((adjusted_lenhei / 100) ** 2)
        
        # Chuyển giới tính thành số
        sex_value = 1 if sex.lower() == "male" else 2 if sex.lower() == "female" else None
        
        # Tính toán Z-score cho các chỉ số
        bmi_age = calculate_zscore(growthstandards["bmi"], age_days, sex_value, bmi)
        wei = calculate_zscore(growthstandards["weight"], age_days, sex_value, weight)
        lenhei_age = calculate_zscore(growthstandards["length"], age_days, sex_value, adjusted_lenhei)
        wfl = calculate_zscore_weight_for_lenhei(adjusted_lenhei, sex_value, weight, age_days=age_days, lenhei_unit=measure)

        # Return results if all Z-scores are calculated successfully
        if all(v is not None for v in [bmi_age, wei, lenhei_age, wfl]):
            return jsonify({
                "bmi": round(bmi, 2),
                "bmi_age": round(bmi_age, 2),
                "wei": round(wei, 2),
                "lenhei_age": round(lenhei_age, 2),
                "wfl": round(wfl, 2),
            })
        else:
            return jsonify({"error": "Không tìm thấy dữ liệu phù hợp"}), 400
    else:
        return send_from_directory(os.getcwd(), 'zscore-calculator.html')
        
# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

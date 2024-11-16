from flask import Flask, request, jsonify, send_from_directory
from drawchart import draw_bmi_chart
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

# Hàm tính Z-score
def compute_zscore(y, m, l, s):
    return np.where(l != 0, ((y / m)**l - 1) / (s * l), np.log(y / m) / s)


# Hàm tính Z-score điều chỉnh khi vượt ngưỡng
def compute_zscore_adjusted(y, m, l, s):
    def calc_sd(sd_val):
        return m * ((1 + l * s * sd_val)**(1 / l))
    
    zscore = compute_zscore(y, m, l, s)
    SD3pos = calc_sd(3)
    SD3neg = calc_sd(-3)
    SD23pos = SD3pos - calc_sd(2)
    SD23neg = calc_sd(-2) - SD3neg
    
    zscore = np.where((~np.isnan(zscore)) & (zscore > 3),
                      3 + (y - SD3pos) / SD23pos,
                      zscore)
    zscore = np.where((~np.isnan(zscore)) & (zscore < -3),
                      -3 + (y - SD3neg) / SD23neg,
                      zscore)
    return zscore

# Hàm áp dụng Z-score và tiêu chuẩn tăng trưởng
def apply_zscore_and_growthstandards(zscore_fun, growthstandards, age_in_days, sex, measure):
    # Đảm bảo đầu vào là dạng mảng numpy để tránh lỗi scalar
    input_df = pd.DataFrame({
        'measure': np.array([measure]),
        'age_in_days': np.array([age_in_days]),
        'sex': np.array([sex])
    })
    merged_df = pd.merge(input_df, growthstandards, how='left', left_on=['age_in_days', 'sex'], right_on=['age', 'sex'])
    
    y = merged_df['measure']
    m = merged_df['m']
    l = merged_df['l']
    s = merged_df['s']
    
    # Tính Z-score
    zscore = zscore_fun(y, m, l, s)
    
    return np.round(zscore, 2)

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

    # Bước 3: Hợp nhất dữ liệu wfl và wfh
    growthstandards_wfl = growthstandards['wfl'].copy()
    growthstandards_wfh = growthstandards['wfh'].copy()
    growthstandards_wfl.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growthstandards_wfh.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growth_data = pd.concat([growthstandards_wfl, growthstandards_wfh])
    growth_data['lorh'] = growth_data['lorh'].str.lower()

   # Bước 4: Xác định chuẩn để sử dụng (wfl hoặc wfh) dựa trên age_days
    join_on_l = ((age_days is not None and age_days < 731) or
                 (age_days is None and lenhei_unit == "l") or
                 (age_days is None and lenhei_unit is None and lenhei < 87))
    join_on_h = ((age_days is not None and age_days >= 731) or
                 (age_days is None and lenhei_unit == "h") or
                 (age_days is None and lenhei_unit is None and lenhei >= 87))

    # Chọn chuẩn phù hợp từ growth_data
    subset_low = growth_data[(growth_data['sex'] == sex) & (growth_data['lenhei'] == low_lenhei) & (growth_data['lorh'] == ('l' if join_on_l else 'h'))]
    subset_upp = growth_data[(growth_data['sex'] == sex) & (growth_data['lenhei'] == upp_lenhei) & (growth_data['lorh'] == ('l' if join_on_l else 'h'))]

    # Kiểm tra nội suy cho các giá trị m, l, s
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
    z_score = compute_zscore_adjusted(weight, m, l, s)
    return z_score

        
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        sex = request.form.get("sex")
        age_days = round_up(float(request.form.get("ageInDays")))
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        measure = request.form.get("measure", "h").lower()
        age_months = age_days / 30.4375
        # Điều chỉnh chiều dài/chiều cao
        adjusted_lenhei = adjust_lenhei(age_days, measure, height)
        
        # Tính BMI
        bmi = weight / ((adjusted_lenhei / 100) ** 2)
        
        # Chuyển giới tính thành số
        sex_value = 1 if sex.lower() == "male" else 2 if sex.lower() == "female" else None
        
        # Gọi hàm vẽ biểu đồ và lấy JSON
        chart_json = draw_bmi_chart(bmi, age_months, sex_value)
        
        # Tính toán Z-score cho các chỉ số
        bmi_age = apply_zscore_and_growthstandards(compute_zscore_adjusted, growthstandards["bmi"], age_days, sex_value, bmi)
        wei = apply_zscore_and_growthstandards(compute_zscore_adjusted, growthstandards["weight"], age_days, sex_value, weight)
        lenhei_age = apply_zscore_and_growthstandards(compute_zscore_adjusted, growthstandards["length"], age_days, sex_value, adjusted_lenhei)
        wfl = calculate_zscore_weight_for_lenhei(adjusted_lenhei, sex_value, weight, age_days=age_days, lenhei_unit=measure)

        if all(v is not None for v in [bmi_age, wei, lenhei_age, wfl]):
            return jsonify({
                "bmi": round(bmi, 2),
                "bmi_age": round(float(bmi_age[0]), 2) if isinstance(bmi_age, np.ndarray) else round(bmi_age, 2),
                "wei": round(float(wei[0]), 2) if isinstance(wei, np.ndarray) else round(wei, 2),
                "lenhei_age": round(float(lenhei_age[0]), 2) if isinstance(lenhei_age, np.ndarray) else round(lenhei_age, 2),
                "wfl": round(float(wfl), 2) if isinstance(wfl, (np.ndarray, np.float64)) else round(wfl, 2),
                "chart_data":chart_json
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


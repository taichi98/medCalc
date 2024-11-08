from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import math
import os

app = Flask(__name__)

# Hàm để đọc dữ liệu chuẩn từ các file txt
def make_standard(name):
    path = f"growthstandards/{name}.txt"
    return pd.read_csv(path, sep='\t', dtype={'sex': int, 'age': int})

# Tải các bảng dữ liệu tiêu chuẩn
growthstandards_bmianthro = make_standard("bmianthro")
growthstandards_weianthro = make_standard("weianthro")
growthstandards_lenanthro = make_standard("lenanthro")
growthstandards_hcanthro = make_standard("hcanthro")
growthstandards_wflanthro = make_standard("wflanthro")
growthstandards_wfhanthro = make_standard("wfhanthro")

# Hàm tính Z-score cho BMI theo tuổi
def calculate_zscore_bmi(age, sex, bmi):
    # Lọc dữ liệu theo giới tính và tuổi
    subset = growthstandards_bmianthro[(growthstandards_bmianthro['sex'] == sex) & 
                                       (growthstandards_bmianthro['age'] == age)]
    
    if not subset.empty:
        l = subset.iloc[0]['l']
        m = subset.iloc[0]['m']
        s = subset.iloc[0]['s']
        
        # Tính Z-score
        bmi_age = ((bmi / m)**l - 1) / (s * l)
        return bmi_age
    else:
        return None

def calculate_zscore_weight(age, sex, weight):
    subset = growthstandards_weianthro[(growthstandards_weianthro['sex'] == sex) & 
                                       (growthstandards_weianthro['age'] == age)]
    
    if not subset.empty:
        l = subset.iloc[0]['l']
        m = subset.iloc[0]['m']
        s = subset.iloc[0]['s']
        
        # Calculate Z-score
        wei = ((weight / m)**l - 1) / (s * l)
        return wei
    else:
        return None
# Hàm tính Z-score cho chiều dài/chiều cao theo tuổi
def calculate_zscore_lenhei(age, sex, lenhei):
    subset = growthstandards_lenanthro[(growthstandards_lenanthro['sex'] == sex) & 
                                       (growthstandards_lenanthro['age'] == age)]
    if not subset.empty:
        l = subset.iloc[0]['l']
        m = subset.iloc[0]['m']
        s = subset.iloc[0]['s']
        lenhei_age = ((lenhei / m)**l - 1) / (s * l)
        return lenhei_age
    else:
        return None

# Hàm tính Z-score cho Weight-for-Length/Height theo chiều dài/chiều cao
def calculate_zscore_weight_for_lenhei(weight, lenhei, lenhei_unit, age_days, sex):
    # Điều kiện tham chiếu tiêu chuẩn dựa trên tuổi và đơn vị đo
    join_on_l = age_days < 731 or (lenhei_unit == "l" or (lenhei < 87))
    join_on_h = age_days >= 731 or (lenhei_unit == "h" or (lenhei >= 87))
    
    # Điều chỉnh độ dài để nội suy
    low_lenhei = int(lenhei * 10) / 10
    upp_lenhei = (int(lenhei * 10) + 1) / 10
    diff_lenhei = (lenhei - low_lenhei) / 0.1
    
    growthstandards = pd.concat([growthstandards_wflanthro, growthstandards_wfhanthro])
    growthstandards["lorh"] = growthstandards["lorh"].str.lower()
    
    # Lọc theo giới tính và giá trị length/height gần nhất
    subset_lower = growthstandards[(growthstandards["sex"] == sex) &
                                   (growthstandards["lenhei"] == low_lenhei) &
                                   (growthstandards["lorh"] == ("l" if join_on_l else "h"))]
    subset_upper = growthstandards[(growthstandards["sex"] == sex) &
                                   (growthstandards["lenhei"] == upp_lenhei) &
                                   (growthstandards["lorh"] == ("l" if join_on_l else "h"))]
    if subset_lower.empty or subset_upper.empty:
        return None

    # Nội suy các giá trị l, m, s
    l = subset_lower["l"].values[0] + diff_lenhei * (subset_upper["l"].values[0] - subset_lower["l"].values[0])
    m = subset_lower["m"].values[0] + diff_lenhei * (subset_upper["m"].values[0] - subset_lower["m"].values[0])
    s = subset_lower["s"].values[0] + diff_lenhei * (subset_upper["s"].values[0] - subset_lower["s"].values[0])

    # Tính Z-score
    weight_lenhei = ((weight / m) ** l - 1) / (s * l)
    return weight_lenhei
    
# Số ngày trung bình trong một tháng theo WHO
ANTHRO_DAYS_OF_MONTH = 30.4375

def round_up(x):
    # Kiểm tra xem x có phải là số và các phần tử không âm
    if isinstance(x, (int, float)) and x >= 0:
        x_rounded = math.floor(x)
        rest = x - x_rounded
        # Làm tròn lên nếu phần thập phân >= 0.5
        if rest >= 0.5:
            x_rounded += 1
        return x_rounded
    elif isinstance(x, list):  # Trường hợp là danh sách các số
        x_rounded_list = []
        for val in x:
            if val >= 0:
                x_rounded = math.floor(val)
                rest = val - x_rounded
                if rest >= 0.5:
                    x_rounded += 1
                x_rounded_list.append(x_rounded)
        return x_rounded_list
    else:
        raise ValueError("Giá trị phải là số dương hoặc danh sách các số dương.")

def age_to_days(age, is_age_in_month):
    if is_age_in_month:
        res = age * ANTHRO_DAYS_OF_MONTH
    else:
        res = age
    return int(round_up(res))

# Hàm điều chỉnh chiều dài/chiều cao theo tuổi và theo cách đo
def adjust_lenhei(age_in_days, measure, lenhei):
    age_in_days = round_up(age_in_days)
    if age_in_days < 731 and measure == "h":
        lenhei += 0.7
    elif age_in_days >= 731 and measure == "l":
        lenhei -= 0.7
    return lenhei

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        sex = request.form.get("sex")
        #age_months = int(request.form.get("age"))  # Nhận tuổi theo tháng
        age_days = int(request.form.get("ageInDays"))
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        measure = request.form.get("measure", "h").lower()  # Nhận dạng đo là "l" hoặc "h"
        # Điều chỉnh chiều dài/chiều cao dựa trên đơn vị đo
        adjusted_lenhei = adjust_lenhei(age_days, measure, height)
        # Tính BMI
        bmi = weight / ((adjusted_lenhei / 100) ** 2)
        # Chuyển đổi giới tính thành dạng số (1 = Nam, 2 = Nữ)
        sex_value = 1 if sex.lower() == "male" else 2 if sex.lower() == "female" else None
        #age_days = age_to_days(age_months, is_age_in_month=True)
        
        # Tính toán Z-score
        bmi_age = calculate_zscore_bmi(age_days, sex_value, bmi)
        wei = calculate_zscore_weight(age_days, sex_value, weight)
        lenhei_age = calculate_zscore_lenhei(age_days, sex_value, adjusted_lenhei)
        #weight_lenhei = calculate_zscore_weight_for_lenhei(weight, adjusted_lenhei, measure, age_days, sex_value)
        # Trả kết quả
        if all(v is not None for v in [bmi_age, wei, lenhei_age, zscore_weight_lenhei]):
            return jsonify({
                "bmi": round(bmi, 2),
                "bmi_age": round(bmi_age, 2),
                "wei": round(wei, 2),
                "lenhei_age": round(lenhei_age, 2),
                "weight_lenhei": round(111, 2)
            })
        else:
            return jsonify({"error": "Không tìm thấy dữ liệu phù hợp"}), 400
    else:
        # Trả về trang HTML `zscore-calculator.html` cho yêu cầu GET
        return send_from_directory(os.getcwd(), 'zscore-calculator.html')
        
# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

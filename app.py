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

        # Tính BMI
        bmi = weight / ((height / 100) ** 2)
        
        # Chuyển đổi giới tính thành dạng số (1 = Nam, 2 = Nữ)
        sex_value = 1 if sex.lower() == "male" else 2 if sex.lower() == "female" else None

        #age_days = age_to_days(age_months, is_age_in_month=True)
        
        # Tính toán Z-score
        bmi_age = calculate_zscore_bmi(age_days, sex_value, bmi)
        wei = calculate_zscore_weight(age_days, sex_value, weight)
        
        if bmi_age is not None and wei is not None:
            return jsonify({"bmi": round(bmi, 2), "bmi_age": round(bmi_age, 2), "wei": round(wei, 2)})
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

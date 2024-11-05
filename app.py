from flask import Flask, request, jsonify, render_template
import pandas as pd
import math

app = Flask(__name__)

# Hàm để đọc dữ liệu chuẩn từ các file txt
def make_standard(name):
    path = f"growthstandards/{name}.txt"
    return pd.read_csv(path, sep='\t', dtype={'sex': int, 'age': int})

# Tải các bảng dữ liệu tiêu chuẩn
growthstandards_bmianthro = make_standard("bmianthro")

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
        z_score = ((bmi / m)**l - 1) / (s * l)
        return z_score
    else:
        return None

@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        sex = request.form.get("sex")
        age = int(request.form.get("age"))
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))

        # Tính BMI
        bmi = weight / ((height / 100) ** 2)
        
        # Chuyển đổi giới tính thành dạng số (1 = Nam, 2 = Nữ)
        sex_value = 1 if sex.lower() == "male" else 2
        
        # Tính toán Z-score
        z_score = calculate_zscore_bmi(age, sex_value, bmi)
        
        if z_score is not None:
            return jsonify({"bmi": round(bmi, 2), "z_score": z_score})
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

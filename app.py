from flask import Flask, request, jsonify, send_from_directory
import os
import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects import pandas2ri

app = Flask(__name__)

# Đường dẫn tới các file RDS và R script
list_standards_path = os.path.join('data', 'standards.rds')
macro_z_path = "macro-z.R"
functions_z_path = "functions-z.R"

# Load các file R
robjects.r(f"source('{macro_z_path}')")
robjects.r(f"source('{functions_z_path}')") 

# Kích hoạt chuyển đổi tự động giữa pandas và R data frames
pandas2ri.activate()

# Load file RDS
list_standards = r['readRDS'](list_standards_path)

# Function để tính toán Z-scores
def calculate_z_scores(sex, age, height, weight):
    # Prepare data as a DataFrame in R
    input_data = robjects.DataFrame({
        "age_in_days": [age * 30],  # Convert months to days
        "sex": [sex],
        "height": [height],
        "weight": [weight]
    })

    # Lấy giá trị từ list_standards
    growth_standard = list_standards.rx2("lenanthro")  # Giả sử lenanthro chứa các chuẩn chiều cao
    measure = "height"  # Tên biến chiều cao
    zscore_name = "zlen"  # Tên biến lưu Z-score chiều cao
    flag_name = "zlen_flag"  # Tên biến lưu cờ cho Z-score chiều cao
    flag_max = 6  # Ngưỡng cờ tối đa
    condition = "!is.na(data[[agevar]]) & data[[agevar]] >= 0 & data[[agevar]] <= 1856"  # Điều kiện

    # Gọi hàm MakeZScores1 từ R
    z_scores = r['MakeZScores1'](input_data, growth_standard, measure, zscore_name, flag_name, flag_max, condition, agevar="age_in_days", sexvar="sex")

    return z_scores

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route('/zscore-calculator', methods=['GET', 'POST'])
def zscore_calculator():
    if request.method == 'POST':
        sex = request.form.get('sex')
        age = float(request.form.get('age'))
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))

        # Tính toán Z-scores bằng hàm R
        z_scores = calculate_z_scores(sex, age, height, weight)

        return jsonify({
            'zlen': z_scores.rx2('zlen')[0],
            'zlen_flag': z_scores.rx2('zlen_flag')[0]
        })

    return send_from_directory(os.getcwd(), 'zscore-calculator.html')

# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

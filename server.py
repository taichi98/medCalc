from flask import Flask, request, jsonify
import pandas as pd
import rpy2.robjects as robjects

app = Flask(__name__)

# Load RDS file in R and expose via Python using rpy2
robjects.r('''
  load_standards <- function() {
    list_standards <- readRDS(file.path("data", "standards.rds"))
    list_standards
  }
''')
load_standards = robjects.globalenv['load_standards']
standards = load_standards()

def calculate_z_score(x, l, m, s):
    if l != 0:
        z = ((x / m) ** l - 1) / (l * s)
    else:
        z = (x - m) / s
    return z

@app.route('/calculate_zscore', methods=['POST'])
def calculate_zscore():
    data = request.json
    age = data['age']
    sex = data['sex']
    height = data['height']
    weight = data['weight']

    # Lọc dữ liệu từ standards để lấy các giá trị LMS cho giới tính và độ tuổi phù hợp
    # Giả sử standards là một DataFrame hoặc một danh sách có cấu trúc tương tự với các cột 'age', 'sex', 'L', 'M', 'S'
    lms_data_len = standards[standards['measure'] == 'length'].loc[(standards['age'] == age) & (standards['sex'] == sex)]
    lms_data_wei = standards[standards['measure'] == 'weight'].loc[(standards['age'] == age) & (standards['sex'] == sex)]
    lms_data_bmi = standards[standards['measure'] == 'bmi'].loc[(standards['age'] == age) & (standards['sex'] == sex)]

    # Lấy các giá trị L, M, S cho từng chỉ số từ dữ liệu tiêu chuẩn
    zlen = calculate_z_score(height, lms_data_len['L'].values[0], lms_data_len['M'].values[0], lms_data_len['S'].values[0])
    zwei = calculate_z_score(weight, lms_data_wei['L'].values[0], lms_data_wei['M'].values[0], lms_data_wei['S'].values[0])

    # Tính BMI từ chiều cao và cân nặng
    bmi = weight / ((height / 100) ** 2)
    zbmi = calculate_z_score(bmi, lms_data_bmi['L'].values[0], lms_data_bmi['M'].values[0], lms_data_bmi['S'].values[0])

    # Trả về kết quả dưới dạng JSON
    result = {
        "zlen": zlen,
        "zwei": zwei,
        "zbmi": zbmi
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

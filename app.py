from flask import Flask, request, jsonify, render_template
import rpy2.robjects as robjects
import os

app = Flask(__name__)

# Đường dẫn tới file standards.rds
standards_path = os.path.join('data', 'standards.rds')

# Hàm khởi tạo R và đọc file standards.rds
robjects.r['readRDS'](standards_path)
robjects.r('''\
list_standards <- readRDS(file.path("data", "standards.rds"))

CalculateZScores <- function(sex, age_in_days, height, weight) {
    # Kiểm tra dữ liệu đầu vào
    if (is.na(sex) || is.na(age_in_days) || is.na(height) || is.na(weight)) {
        stop("Giá trị đầu vào không hợp lệ.")
    }

    # Chuyển đổi giới tính
    csex <- ifelse(sex == "male", 1, ifelse(sex == "female", 2, NA))
    
    # Chuẩn hóa dữ liệu
    clenhei <- ifelse(age_in_days < 731, height + 0.7, height - 0.7)
    cbmi <- weight / (clenhei / 100)^2
    
    # Tính toán z-scores
    zlen <- MakeZScores1(list_standards[["lenanthro"]], "clenhei", "zlen", "zlen_flag", 6, age_in_days, csex, "!is.na(age_in_days) & age_in_days >= 0 & age_in_days <= 1856")
    zwei <- MakeZScores2(list_standards[["weianthro"]], weight, "zwei", "zwei_flag", 5, -6, age_in_days, csex, NULL, '!is.na(age_in_days) & age_in_days >= 0 & age_in_days <= 1856')
    zbmi <- MakeZScores2(list_standards[["bmianthro"]], cbmi, "zbmi", "zbmi_flag", 5, age_in_days, csex, NULL, '!is.na(age_in_days) & age_in_days >= 0 & age_in_days <= 1856')
    
    # Trả về kết quả
    list(zlen = zlen, zwei = zwei, zbmi = zbmi)
}
''')

@app.route('/')
def index():
    return render_template('zscore-calculator.html')

@app.route('/calculate_zscore', methods=['POST'])
def calculate_zscore():
    try:
        sex = request.form['sex']
        age = int(request.form['age']) * 30.44  # Chuyển tuổi từ tháng sang ngày
        height = float(request.form['height'])
        weight = float(request.form['weight'])

        # Gọi hàm R để tính z-scores
        calculate_zscore_r = robjects.globalenv['CalculateZScores']
        results = calculate_zscore_r(sex, age, height, weight)

        # Chuyển đổi kết quả từ R sang Python
        zlen = float(results[0][0])  # Chỉ lấy giá trị đầu tiên
        zwei = float(results[1][0])
        zbmi = float(results[2][0])

        return jsonify({
            'Length-for-Age Z-Score': zlen,
            'Weight-for-Age Z-Score': zwei,
            'BMI-for-Age Z-Score': zbmi
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

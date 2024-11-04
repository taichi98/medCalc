from flask import Flask, request, jsonify, send_from_directory
import os
import rpy2.robjects as robjects
from rpy2.robjects import r

app = Flask(__name__)

# Đảm bảo bạn có đường dẫn đúng đến file standards.rds
standards_path = os.path.join('data', 'standards.rds')

# Hàm tính Z-score (cần thay đổi cho phù hợp với logic của bạn)
def calculate_z_score(sex, age, height, weight):
    # Logic tính toán Z-score của bạn ở đây
    # Trả về giá trị Z-score (ví dụ: 0.5)
    return 0.5  # Thay đổi giá trị này với kết quả thực tế
  
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')
@app.route('/zscore-calculator', methods=['GET'])
def zscore_calculator():
    return send_from_directory(os.getcwd(), 'zscore-calculator.html')

@app.route('/zscore-calculator', methods=['GET', 'POST'])
def zscore_calculator():
    if request.method == 'POST':
        sex = request.form.get('sex')
        age = float(request.form.get('age'))
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))

        # Tính Z-score
        z_score = calculate_z_score(sex, age, height, weight)

        return jsonify({'z_score': z_score})

    return send_from_directory(os.getcwd(), 'zscore-calculator.html')

# Thêm route để phục vụ các tệp tĩnh
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

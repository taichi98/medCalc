from flask import Flask, request, jsonify, render_template
import rpy2.robjects as robjects
import os

app = Flask(__name__, template_folder='.')

# Đường dẫn tới file standards.rds
standards_path = os.path.join('data', 'standards.rds')

# Hàm khởi tạo R và đọc file standards.rds
robjects.r['readRDS'](standards_path)
robjects.r('''
list_standards <- readRDS(file.path("data", "standards.rds"))
''')

def calculate_z_scores(data):
    # Chuyển đổi chiều cao và cân nặng sang kiểu số
    data['weight'] = pd.to_numeric(data['weight'], errors='coerce')
    data['length'] = pd.to_numeric(data['length'], errors='coerce')
    data['age_in_days'] = pd.to_numeric(data['age_in_days'], errors='coerce')

    # Các giá trị mặc định
    data['csex'] = data['sex'].apply(lambda x: 1 if x.lower() in ['m', '1'] else (2 if x.lower() in ['f', '2'] else np.nan))
    
    # Tính toán z-scores cho từng chỉ số
    data['zlen'] = compute_z_score(data['length'], list_standards['lenanthro'], data['age_in_days'], data['csex'])
    data['zwei'] = compute_z_score(data['weight'], list_standards['weianthro'], data['age_in_days'], data['csex'])
    data['zbmi'] = compute_z_score(data['weight'] / (data['length']/100) ** 2, list_standards['bmianthro'], data['age_in_days'], data['csex'])
    
    # Tính toán z-scores cho chiều dài và cân nặng theo chiều cao
    data['zwfl'] = compute_wfl(data, list_standards['wflanthro'])
    data['zwfh'] = compute_wfh(data, list_standards['wfhanthro'])
    
    return data

def compute_z_score(measure, standards, age_in_days, sex):
    # Đây là hàm giả định để tính toán z-score dựa trên tiêu chuẩn
    # Thay thế bằng logic cụ thể theo yêu cầu của bạn
    # Logic z-score sẽ được tính toán tại đây
    return (measure - standards.mean()) / standards.std()

def compute_wfl(data, standards):
    # Logic tính toán z-score cho cân nặng chiều dài
    return (data['weight'] / (data['length'] / 100) ** 2 - standards.mean()) / standards.std()

def compute_wfh(data, standards):
    # Logic tính toán z-score cho cân nặng chiều cao
    return (data['weight'] / (data['height'] / 100) ** 2 - standards.mean()) / standards.std()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/zscore', methods=['POST'])
def calculate():
    # Nhận dữ liệu từ form
    data = request.form.to_dict()
    df = pd.DataFrame([data])
    
    # Tính toán z-scores
    result = calculate_z_scores(df)
    
    # Chuyển đổi kết quả thành HTML hoặc JSON để hiển thị
    return render_template('zscore-calculator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

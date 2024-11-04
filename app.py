from flask import Flask, request, jsonify, render_template
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import rpy2.robjects.vectors as rv

app = Flask(__name__, template_folder='.')

# Tải thư viện anthro từ WHO
try:
    anthro = importr("anthro")
except:
    raise ImportError("Bạn cần cài đặt gói 'anthro' trong môi trường R.")

# Hàm tính Z-score dựa trên anthro
def calculate_z_scores(sex, age_months, height, weight):
    # Chuẩn bị dữ liệu đầu vào
    sex_r = rv.FactorVector(["M" if sex.lower() == "male" else "F"])
    age_months_r = rv.FloatVector([age_months])
    height_r = rv.FloatVector([height])
    weight_r = rv.FloatVector([weight])
    
    # Gọi hàm anthro từ R
    result = anthro.anthro_zscores(sex=sex_r, age=age_months_r, lenhei=height_r, weight=weight_r)
    
    # Chuyển đổi kết quả từ R sang Python dictionary
    z_scores = {
        "Length-for-Age Z-Score": result[0][0],
        "Weight-for-Age Z-Score": result[1][0],
        "BMI-for-Age Z-Score": result[3][0]
    }
    return z_scores

@app.route('/')
def index():
    return render_template('zscore-calculator.html')

@app.route('/calculate_zscore', methods=['POST'])
def calculate():
    try:
        # Nhận dữ liệu từ form
        sex = request.form['sex']
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        
        # Tính Z-score
        result = calculate_z_scores(sex, age, height, weight)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)

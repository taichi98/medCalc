from flask import Flask, request, jsonify, send_from_directory
import os
import rpy2.robjects as robjects
from rpy2.robjects import r
from rpy2.robjects import pandas2ri

app = Flask(__name__)

# Đường dẫn tới các file R và chuẩn RDS
list_standards_path = os.path.join('data', 'standards.rds')
macro_z_path = "macro-z.R"
functions_z_path = "functions-z.R"

# Load các file R
robjects.r(f"source('{macro_z_path}')")
robjects.r(f"source('{functions_z_path}')")

# Kích hoạt tự động chuyển đổi giữa pandas và R data frames
pandas2ri.activate()

# Load the R standards file
standards_data = r['readRDS'](list_standards_path)

# Function to calculate Z-scores using R
def calculate_z_scores(sex, age, height, weight):
    # Prepare data as a DataFrame in R
    input_data = robjects.DataFrame({
        "age_in_days": [age * 30],  # Convert months to days
        "sex": [sex],
        "height": [height],
        "weight": [weight],
        "age_group": [None],  # If age group is needed
        "oedema": [None],  # Assuming no oedema
    })

    # Call the R function
    z_scores = r['CalculateZScores'](input_data, sex="sex", weight="weight", lenhei="height", lenhei_unit="h")  # Assuming 'h' for height
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

        # Calculate Z-scores using the R function
        z_scores = calculate_z_scores(sex, age, height, weight)

        return jsonify({
            'zwfl': z_scores.rx2('zwfl')[0],
            'zbmi': z_scores.rx2('zbmi')[0],
            'zlen': z_scores.rx2('zlen')[0],
            'zwei': z_scores.rx2('zwei')[0]
        })

    return send_from_directory(os.getcwd(), 'zscore-calculator.html')

# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

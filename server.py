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

@app.route('/calculate_zscore', methods=['POST'])
def calculate_zscore():
    data = request.json
    age = data['age']
    sex = data['sex']
    height = data['height']
    weight = data['weight']

    # Implement the Z-score calculation using standards data
    # Assuming standards has columns for age, sex, and the LMS values (lambda, mu, sigma)

    result = {
        "zlen": zlen,
        "zwei": zwei,
        "zbmi": zbmi
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

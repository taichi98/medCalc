from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import numpy as np
import math
import os

app = Flask(__name__)

# Hàm để đọc dữ liệu chuẩn từ các file txt
def make_standard(name):
    path = f"growthstandards/{name}.txt"
    return pd.read_csv(path, sep='\t', dtype={'sex': int, 'age': int})

# Tải các bảng dữ liệu tiêu chuẩn
growthstandards = {
    "bmi": make_standard("bmianthro"),
    "weight": make_standard("weianthro"),
    "length": make_standard("lenanthro"),
    "head": make_standard("hcanthro"),
    "wfl": make_standard("wflanthro"),
    "wfh": make_standard("wfhanthro")
}

# Hàm tính Z-score chung
def calculate_zscore(data, age, sex, measure_value):
    subset = data[(data['sex'] == sex) & (data['age'] == age)]
    if not subset.empty:
        l = subset.iloc[0]['l']
        m = subset.iloc[0]['m']
        s = subset.iloc[0]['s']
        z_score = ((measure_value / m) ** l - 1) / (s * l)
        return z_score
    else:
        return None

# Số ngày trung bình trong một tháng theo WHO
ANTHRO_DAYS_OF_MONTH = 30.4375

def round_up(x):
    if isinstance(x, (int, float)) and x >= 0:
        x_rounded = math.floor(x)
        rest = x - x_rounded
        if rest >= 0.5:
            x_rounded += 1
        return x_rounded
    elif isinstance(x, list):  
        return [round_up(val) for val in x if val >= 0]
    else:
        raise ValueError("Giá trị phải là số dương hoặc danh sách các số dương.")

def age_to_days(age, is_age_in_month):
    return int(round_up(age * ANTHRO_DAYS_OF_MONTH if is_age_in_month else age))

# Hàm điều chỉnh chiều dài/chiều cao theo tuổi và cách đo
def adjust_lenhei(age_in_days, measure, lenhei):
    age_in_days = round_up(age_in_days)
    if age_in_days < 731 and measure == "h":
        lenhei += 0.7
    elif age_in_days >= 731 and measure == "l":
        lenhei -= 0.7
    return lenhei

# Hàm tính z-score weight-for-length/height
def anthro_zscore_weight_for_lenhei(weight, lenhei, lenhei_unit, age_in_days, age_in_months, sex,
                                    growthstandards_wfl=None, growthstandards_wfh=None):
    # Input validation
    assert isinstance(weight, (float, int, np.ndarray))
    assert isinstance(lenhei, (float, int, np.ndarray))
    assert isinstance(age_in_months, (float, int))
    assert_valid_sex(sex)
    age_in_days = assert_valid_age_in_days(age_in_days)
    assert_growthstandards(growthstandards_wfl)
    assert_growthstandards(growthstandards_wfh)

    n = len(lenhei)

    # Clean weight/lenhei
    weight = np.where((weight < 0.9) | (weight > 58.0), np.nan, weight)
    lenhei = np.where((lenhei < 38.0) | (lenhei > 150.0), np.nan, lenhei)

    # Interpolate lenhei under certain conditions
    low_lenhei = np.floor(lenhei * 10) / 10
    upp_lenhei = (np.floor(lenhei * 10) + 1) / 10
    diff_lenhei = (lenhei - low_lenhei) / 0.1

    # Harmonize growthstandards for joining on both units
    growthstandards_wfl.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growthstandards_wfh.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growthstandards = pd.concat([growthstandards_wfl, growthstandards_wfh], ignore_index=True)
    growthstandards["lorh"] = growthstandards["lorh"].str.lower()

    # Determine which standards to join on
    join_on_l = (
        (not np.isnan(age_in_days) and age_in_days < 731) or
        (np.isnan(age_in_days) and lenhei_unit == "l") or
        (np.isnan(age_in_days) and lenhei < 87)
    )
    join_on_h = (
        (not np.isnan(age_in_days) and age_in_days >= 731) or
        (np.isnan(age_in_days) and lenhei_unit == "h") or
        (np.isnan(age_in_days) and lenhei >= 87)
    )

    # Prepare input DataFrame
    input_df = pd.DataFrame({
        "weight": weight,
        "sex": sex,
        "lenhei_unit": lenhei_unit,
        "low_lenhei": low_lenhei,
        "upp_lenhei": upp_lenhei,
        "diff_lenhei": diff_lenhei,
        "ordering": range(n),
        "join_col": np.where(join_on_l, "l", np.where(join_on_h, "h", np.nan))
    })

    # Merge with growth standards
    merged_df = input_df.merge(
        growthstandards, left_on=["sex", "low_lenhei", "join_col"],
        right_on=["sex", "lenhei", "lorh"], how="left", suffixes=("", "_lower")
    ).merge(
        growthstandards, left_on=["sex", "upp_lenhei", "join_col"],
        right_on=["sex", "lenhei", "lorh"], how="left", suffixes=("", "_upper")
    ).sort_values("ordering")

    y = merged_df["weight"]
    m = np.where(diff_lenhei > 0,
                 merged_df["m"] + diff_lenhei * (merged_df["m_upper"] - merged_df["m"]),
                 merged_df["m"]).astype(float)
    l = np.where(diff_lenhei > 0,
                 merged_df["l"] + diff_lenhei * (merged_df["l_upper"] - merged_df["l"]),
                 merged_df["l"]).astype(float)
    s = np.where(diff_lenhei > 0,
                 merged_df["s"] + diff_lenhei * (merged_df["s_upper"] - merged_df["s"]),
                 merged_df["s"]).astype(float)

    # Calculate zscore
    zscore = compute_zscore_adjusted(y, m, l, s)
    zscore = np.round(zscore, 2)

    # Determine valid zscore conditions
    valid_zscore = (
        (~np.isnan(lenhei)) &
        np.where(join_on_l, (lenhei >= 45) & (lenhei <= 110),
                 np.where(join_on_h, (lenhei >= 65) & (lenhei <= 120), False)) &
        (np.isnan(age_in_days) or (age_in_days <= 1856)) &
        (age_in_months < 60)
    )

    return zscore

        
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), 'index.html')

@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        sex = request.form.get("sex")
        age_days = int(request.form.get("ageInDays"))
        height = float(request.form.get("height"))
        weight = float(request.form.get("weight"))
        measure = request.form.get("measure", "h").lower()
        
        # Điều chỉnh chiều dài/chiều cao
        adjusted_lenhei = adjust_lenhei(age_days, measure, height)
        
        # Tính BMI
        bmi = weight / ((adjusted_lenhei / 100) ** 2)
        
        # Chuyển giới tính thành số
        sex_value = 1 if sex.lower() == "male" else 2 if sex.lower() == "female" else None
        
        # Tính toán Z-score cho các chỉ số
        bmi_age = calculate_zscore(growthstandards["bmi"], age_days, sex_value, bmi)
        wei = calculate_zscore(growthstandards["weight"], age_days, sex_value, weight)
        lenhei_age = calculate_zscore(growthstandards["length"], age_days, sex_value, adjusted_lenhei)
        # Calculate weight-for-length/height Z-score using `anthro_zscore_weight_for_lenhei`
        wfl_zscore = anthro_zscore_weight_for_lenhei(
            weight=weight,
            lenhei=adjusted_lenhei,
            lenhei_unit=measure,
            age_in_days=age_days,
            age_in_months=age_days / ANTHRO_DAYS_OF_MONTH,
            sex=sex_value,
            growthstandards_wfl=growthstandards["wfl"],
            growthstandards_wfh=growthstandards["wfh"]
        )
        # Return results if all Z-scores are calculated successfully
        if all(v is not None for v in [bmi_age, wei, lenhei_age, wfl_zscore]):
            return jsonify({
                "bmi": round(bmi, 2),
                "bmi_age": round(bmi_age, 2),
                "wei": round(wei, 2),
                "lenhei_age": round(lenhei_age, 2),
                "wfl": round(wfl_zscore, 2),
            })
        else:
            return jsonify({"error": "Không tìm thấy dữ liệu phù hợp"}), 400
    else:
        return send_from_directory(os.getcwd(), 'zscore-calculator.html')
        
# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

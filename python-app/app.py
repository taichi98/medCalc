from flask import Flask, request, jsonify, send_from_directory
from drawchart import draw_bmi_chart, draw_wfa_chart, draw_lhfa_chart, draw_wfl_wfh_chart, draw_bmi_chart_above5yr, draw_wfa_chart_above5yr, draw_lhfa_chart_above5yr
from percentilechart import draw_bmi_percentile_chart, draw_wfa_percentile_chart, draw_lhfa_percentile_chart, draw_wfl_wfh_percentile_chart, draw_lhfa_percentile_chart_above5yr, draw_wfa_percentile_chart_above5yr, draw_bmi_percentile_chart_above5yr
from scipy.stats import norm
import pandas as pd
import numpy as np
import math
import os

app = Flask(__name__)

# Số ngày trung bình trong một tháng theo WHO
ANTHRO_DAYS_OF_MONTH = 30.4375


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
    "wfh": make_standard("wfhanthro"),
    "weight_5_plus": make_standard("wfawho2007"),
    "height_5_plus": make_standard("hfawho2007"),
    "bmi_5_plus": make_standard("bfawho2007")
}


# Hàm tính Z-score
def compute_zscore(y, m, l, s):
    return np.where(l != 0, ((y / m)**l - 1) / (s * l), np.log(y / m) / s)


# Hàm tính Z-score điều chỉnh khi vượt ngưỡng
def compute_zscore_adjusted(y, m, l, s):

    def calc_sd(sd_val):
        return m * ((1 + l * s * sd_val)**(1 / l))

    zscore = compute_zscore(y, m, l, s)
    SD3pos = calc_sd(3)
    SD3neg = calc_sd(-3)
    SD23pos = SD3pos - calc_sd(2)
    SD23neg = calc_sd(-2) - SD3neg

    zscore = np.where((~np.isnan(zscore)) & (zscore > 3),
                      3 + (y - SD3pos) / SD23pos, zscore)
    zscore = np.where((~np.isnan(zscore)) & (zscore < -3),
                      -3 + (y - SD3neg) / SD23neg, zscore)
    return zscore


# Hàm áp dụng Z-score và tiêu chuẩn tăng trưởng
def apply_zscore_and_growthstandards(zscore_fun, growthstandards, age_in_days,
                                     sex, measure):
    input_df = pd.DataFrame({
        'measure': np.array([measure]),
        'age_in_days': np.array([age_in_days]),
        'sex': np.array([sex])
    })
    merged_df = pd.merge(input_df,
                         growthstandards,
                         how='left',
                         left_on=['age_in_days', 'sex'],
                         right_on=['age', 'sex'])

    y = merged_df['measure']
    m = merged_df['m']
    l = merged_df['l']
    s = merged_df['s']

    # Tính Z-score
    zscore = zscore_fun(y, m, l, s)

    return np.round(zscore, 2)


def apply_zscore_and_growthstandards_above_5(zscore_fun, growthstandards,
                                             age_in_months, sex, measure):
    # Tính tuổi tháng dưới và trên
    low_age = np.floor(age_in_months)
    upp_age = np.ceil(age_in_months)
    diff_age = age_in_months - low_age

    # Tạo DataFrame đầu vào
    input_df_low = pd.DataFrame({
        'measure': [measure],
        'age': [low_age],
        'sex': [sex]
    })

    input_df_upp = pd.DataFrame({
        'measure': [measure],
        'age': [upp_age],
        'sex': [sex]
    })

    # Ghép dữ liệu từ bảng tăng trưởng
    merged_df_low = pd.merge(input_df_low,
                             growthstandards,
                             how='left',
                             on=['age', 'sex'])
    merged_df_upp = pd.merge(input_df_upp,
                             growthstandards,
                             how='left',
                             on=['age', 'sex'])

    # Nội suy các giá trị l, m, s
    m = np.interp(age_in_months, [low_age, upp_age],
                  [merged_df_low['m'].iloc[0], merged_df_upp['m'].iloc[0]])
    l = np.interp(age_in_months, [low_age, upp_age],
                  [merged_df_low['l'].iloc[0], merged_df_upp['l'].iloc[0]])
    s = np.interp(age_in_months, [low_age, upp_age],
                  [merged_df_low['s'].iloc[0], merged_df_upp['s'].iloc[0]])

    # Tính Z-score
    zscore = zscore_fun(measure, m, l, s)
    return np.round(zscore, 2)


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
        raise ValueError(
            "Giá trị phải là số dương hoặc danh sách các số dương.")


# Hàm điều chỉnh chiều dài/chiều cao theo tuổi và cách đo
def adjust_lenhei(age_in_days, measure, lenhei):
    age_in_days = round_up(age_in_days)
    if age_in_days < 731 and measure == "h":
        lenhei += 0.7
    elif age_in_days >= 731 and measure == "l":
        lenhei -= 0.7
    return lenhei


def calculate_zscore_weight_for_lenhei(lenhei,
                                       sex,
                                       weight,
                                       age_days=None,
                                       lenhei_unit=None):
    # Bước 1: Kiểm tra và làm sạch dữ liệu
    if weight < 0.9 or weight > 58.0:
        return None
    if lenhei < 38.0 or lenhei > 150.0:
        return None

    # Bước 2: Nội suy chiều dài/chiều cao
    low_lenhei = np.trunc(lenhei * 10) / 10
    upp_lenhei = np.trunc(lenhei * 10 + 1) / 10
    diff_lenhei = (lenhei - low_lenhei) / 0.1

    # Bước 3: Hợp nhất dữ liệu wfl và wfh
    growthstandards_wfl = growthstandards['wfl'].copy()
    growthstandards_wfh = growthstandards['wfh'].copy()
    growthstandards_wfl.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growthstandards_wfh.columns = ["sex", "lenhei", "l", "m", "s", "lorh"]
    growth_data = pd.concat([growthstandards_wfl, growthstandards_wfh])
    growth_data['lorh'] = growth_data['lorh'].str.lower()

    # Bước 4: Xác định chuẩn để sử dụng (wfl hoặc wfh) dựa trên age_days
    join_on_l = ((age_days is not None and age_days < 731)
                 or (age_days is None and lenhei_unit == "l")
                 or (age_days is None and lenhei_unit is None and lenhei < 87))
    join_on_h = ((age_days is not None and age_days >= 731)
                 or (age_days is None and lenhei_unit == "h") or
                 (age_days is None and lenhei_unit is None and lenhei >= 87))

    # Chọn chuẩn phù hợp từ growth_data
    subset_low = growth_data[(growth_data['sex'] == sex)
                             & (growth_data['lenhei'] == low_lenhei) &
                             (growth_data['lorh']
                              == ('l' if join_on_l else 'h'))]
    subset_upp = growth_data[(growth_data['sex'] == sex)
                             & (growth_data['lenhei'] == upp_lenhei) &
                             (growth_data['lorh']
                              == ('l' if join_on_l else 'h'))]

    # Kiểm tra nội suy cho các giá trị m, l, s
    if not subset_low.empty and not subset_upp.empty:
        l = subset_low.iloc[0]['l'] + diff_lenhei * (subset_upp.iloc[0]['l'] -
                                                     subset_low.iloc[0]['l'])
        m = subset_low.iloc[0]['m'] + diff_lenhei * (subset_upp.iloc[0]['m'] -
                                                     subset_low.iloc[0]['m'])
        s = subset_low.iloc[0]['s'] + diff_lenhei * (subset_upp.iloc[0]['s'] -
                                                     subset_low.iloc[0]['s'])
    elif not subset_low.empty:
        l, m, s = subset_low.iloc[0]['l'], subset_low.iloc[0][
            'm'], subset_low.iloc[0]['s']
    elif not subset_upp.empty:
        l, m, s = subset_upp.iloc[0]['l'], subset_upp.iloc[0][
            'm'], subset_upp.iloc[0]['s']
    else:
        return None

    # Bước 7: Tính Z-score
    z_score = compute_zscore_adjusted(weight, m, l, s)
    return z_score


# Hàm chuyển đổi Z-score thành Percentile
def zscore_to_percentile(zscore):
    if zscore is None or math.isnan(zscore):
        return None
    return round(norm.cdf(zscore) * 100, 1)

@app.route('/endpoint')
def endpoint():
    return "Hello from Python on Railway!"
    
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), '/php-app/index.php')


@app.route("/zscore-calculator", methods=["GET", "POST"])
def zscore_calculator():
    if request.method == "POST":
        try:
            sex = request.form.get("sex")
            age_days = round_up(float(request.form.get("ageInDays")))
            height = float(request.form.get("height"))
            weight = float(request.form.get("weight"))
            measure = request.form.get("measure", "h").lower()
            age_months = age_days / 30.4375
            is_above_5_years = age_days > 1856
            is_above_10_years = age_days > 3682

            # Điều chỉnh chiều dài/chiều cao
            adjusted_lenhei = adjust_lenhei(age_days, measure, height)

            # Tính BMI
            bmi = weight / ((adjusted_lenhei / 100)**2)

            # Chuyển giới tính thành số
            sex_value = 1 if sex.lower() == "male" else 2 if sex.lower(
            ) == "female" else None

            # Gọi hàm vẽ biểu đồ zscore và nhận JSON cùng cấu hình
            if is_above_5_years:
                bmia_chart_json, bmia_config = draw_bmi_chart_above5yr(
                    bmi, age_months, sex_value)
                wfa_chart_json, wfa_config = draw_wfa_chart_above5yr(
                    weight, age_months, sex_value)
                lhfa_chart_json, lhfa_config = draw_lhfa_chart_above5yr(
                    adjusted_lenhei, age_months, sex_value)
                wflh_chart_json, wflh_config = None, None  # Không vẽ biểu đồ Weight for Length/Height cho trẻ >5 tuổi

                bmia_percentile_chart_json, bmia_percentile_config = draw_bmi_percentile_chart_above5yr(
                    bmi, age_months, sex_value)
                wfa_percentile_chart_json, wfa_percentile_config = draw_wfa_percentile_chart_above5yr(
                    weight, age_months, sex_value)
                lhfa_percentile_chart_json, lhfa_percentile_config = draw_lhfa_percentile_chart_above5yr(
                    adjusted_lenhei, age_months, sex_value)
                wflh_percentile_chart_json, wflh_percentile_config = None, None
            else:
                bmia_chart_json, bmia_config = draw_bmi_chart(
                    bmi, age_months, sex_value)
                wfa_chart_json, wfa_config = draw_wfa_chart(
                    weight, age_months, sex_value)
                lhfa_chart_json, lhfa_config = draw_lhfa_chart(
                    adjusted_lenhei, age_months, sex_value)
                wflh_chart_json, wflh_config = draw_wfl_wfh_chart(
                    weight, adjusted_lenhei, sex_value, measure)
                bmia_percentile_chart_json, bmia_percentile_config = draw_bmi_percentile_chart(
                    bmi, age_months, sex_value)
                wfa_percentile_chart_json, wfa_percentile_config = draw_wfa_percentile_chart(
                    weight, age_months, sex_value)
                lhfa_percentile_chart_json, lhfa_percentile_config = draw_lhfa_percentile_chart(
                    adjusted_lenhei, age_months, sex_value)
                wflh_percentile_chart_json, wflh_percentile_config = draw_wfl_wfh_percentile_chart(
                    weight, adjusted_lenhei, sex_value, measure)

            # Tính toán Z-score cho các chỉ số
            if is_above_5_years:
                bmi_age = apply_zscore_and_growthstandards_above_5(
                    compute_zscore_adjusted, growthstandards["bmi_5_plus"],
                    age_months, sex_value, bmi)

                if is_above_10_years:
                    wei = None  # Trẻ trên 10 tuổi không tính Weight for age
                else:
                    wei = apply_zscore_and_growthstandards_above_5(
                        compute_zscore_adjusted,
                        growthstandards["weight_5_plus"], age_months,
                        sex_value, weight)

                lenhei_age = apply_zscore_and_growthstandards_above_5(
                    compute_zscore_adjusted, growthstandards["height_5_plus"],
                    age_months, sex_value, adjusted_lenhei)
                wfl = None  # Trẻ trên 5 tuổi không tính Weight for Length/Height
            else:
                bmi_age = apply_zscore_and_growthstandards(
                    compute_zscore_adjusted, growthstandards["bmi"], age_days,
                    sex_value, bmi)
                wei = apply_zscore_and_growthstandards(
                    compute_zscore_adjusted, growthstandards["weight"],
                    age_days, sex_value, weight)
                lenhei_age = apply_zscore_and_growthstandards(
                    compute_zscore_adjusted, growthstandards["length"],
                    age_days, sex_value, adjusted_lenhei)
                wfl = calculate_zscore_weight_for_lenhei(adjusted_lenhei,
                                                         sex_value,
                                                         weight,
                                                         age_days=age_days,
                                                         lenhei_unit=measure)

            result_data = {
                "bmi": round(bmi, 2),
                "bmi_age": {
                    "zscore":
                    round(float(bmi_age[0]), 2) if isinstance(
                        bmi_age, np.ndarray) else round(bmi_age, 2),
                    "percentile":
                    zscore_to_percentile(bmi_age[0] if isinstance(
                        bmi_age, np.ndarray) else bmi_age)
                },
                "lenhei_age": {
                    "zscore":
                    round(float(lenhei_age[0]), 2) if isinstance(
                        lenhei_age, np.ndarray) else round(lenhei_age, 2),
                    "percentile":
                    zscore_to_percentile(lenhei_age[0] if isinstance(
                        lenhei_age, np.ndarray) else lenhei_age)
                },
                "charts": {
                    "bmi": {
                        "zscore": {
                            "data": bmia_chart_json,
                            "config": bmia_config
                        },
                        "percentile": {
                            "data": bmia_percentile_chart_json,
                            "config": bmia_percentile_config
                        }
                    },
                    "wfa": {
                        "zscore": {
                            "data": wfa_chart_json,
                            "config": wfa_config
                        },
                        "percentile": {
                            "data": wfa_percentile_chart_json,
                            "config": wfa_percentile_config
                        }
                    },
                    "lhfa": {
                        "zscore": {
                            "data": lhfa_chart_json,
                            "config": lhfa_config
                        },
                        "percentile": {
                            "data": lhfa_percentile_chart_json,
                            "config": lhfa_percentile_config
                        }
                    },
                    "wflh": {
                        "zscore": {
                            "data": wflh_chart_json,
                            "config": wflh_config
                        },
                        "percentile": {
                            "data": wflh_percentile_chart_json,
                            "config": wflh_percentile_config
                        }
                    }
                }
            }

            # Chỉ trả về wfl nếu trẻ dưới 5 tuổi
            if not is_above_5_years:
                result_data["wfl"] = {
                    "zscore":
                    round(float(wfl), 2) if isinstance(
                        wfl, (np.ndarray, np.float64)) else round(wfl, 2),
                    "percentile":
                    zscore_to_percentile(wfl)
                }

            if not is_above_10_years:
                result_data["wei"] = {
                    "zscore":
                    round(float(wei[0]), 2)
                    if isinstance(wei, np.ndarray) else round(wei, 2),
                    "percentile":
                    zscore_to_percentile(
                        wei[0] if isinstance(wei, np.ndarray) else wei)
                }

            return jsonify(result_data)

        except Exception as e:
            return jsonify({"error": str(e)})

    # Trả về tệp HTML cho yêu cầu GET
    return send_from_directory(os.getcwd(), 'zscore-calculator.html')


# Route for serving static files
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.getcwd(), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

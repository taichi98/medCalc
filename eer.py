# eer.py
def calculate_ecg(age, sex):
    """Tính ECG dựa trên tuổi và giới tính."""
    if sex.lower() == "female":
        if age < 0.25:
            return 180
        elif age < 0.5:
            return 60
        elif age < 1:
            return 20
        elif age < 9:
            return 15
        elif age < 14:
            return 30
        else:
            return 20
    elif sex.lower() == "male":
        if age < 0.25:
            return 200
        elif age < 0.5:
            return 50
        elif age < 4:
            return 20
        elif age < 9:
            return 15
        elif age < 14:
            return 25
        else:
            return 20
    else:
        raise ValueError("Invalid gender. Use 'male' or 'female'.")

def calculate_eer(age, height, weight, pal, sex):
    """Tính toán EER dựa trên tuổi, chiều cao, cân nặng, mức độ hoạt động và giới tính."""
    ecg = calculate_ecg(age, sex)  # Lấy giá trị ECG

    if sex.lower() == "female":
        if age <= 2.99:
            eer = -69.15 + (80.0 * age) + (2.65 * height) + (54.15 * weight) + ecg
        elif pal == "inactive":
            eer = 55.59 - (22.25 * age) + (8.43 * height) + (17.07 * weight) + ecg
        elif pal == "lowactive":
            eer = -297.54 - (22.25 * age) + (12.77 * height) + (14.73 * weight) + ecg
        elif pal == "active":
            eer = -189.55 - (22.25 * age) + (11.74 * height) + (18.34 * weight) + ecg
        elif pal == "veryactive":
            eer = -709.59 - (22.25 * age) + (18.22 * height) + (14.25 * weight) + ecg
        else:
            raise ValueError("Invalid PAL level.")
    
    elif sex.lower() == "male":
        if age <= 2.99:
            eer = -716.45 - age + (17.82 * height) + (15.06 * weight) + ecg
        elif pal == "inactive":
            eer = -447.51 + (3.68 * age) + (13.01 * height) + (13.15 * weight) + ecg
        elif pal == "lowactive":
            eer = 19.12 + (3.68 * age) + (8.62 * height) + (20.28 * weight) + ecg
        elif pal == "active":
            eer = -388.19 + (3.68 * age) + (12.66 * height) + (20.46 * weight) + ecg
        elif pal == "veryactive":
            eer = -671.75 + (3.68 * age) + (15.38 * height) + (23.25 * weight) + ecg
        else:
            raise ValueError("Invalid PAL level.")
    
    else:
        raise ValueError("Invalid gender. Use 'male' or 'female'.")

    return round(eer, 2)  # Làm tròn EER

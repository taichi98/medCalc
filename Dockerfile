# Chọn hình ảnh cơ sở (base image)
FROM python:3.9-slim

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào thư mục làm việc
COPY requirements.txt .

# Cài đặt các phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn vào thư mục làm việc
COPY . .

# Chạy ứng dụng Flask
CMD ["python", "app.py"]

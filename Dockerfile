# Sử dụng image cơ bản của Python
FROM python:3.11

# Cài đặt R và các thư viện cần thiết
RUN apt-get update && apt-get install -y r-base

# Cài đặt các gói Python từ requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy mã nguồn vào container
COPY . .

# Đặt biến môi trường cho R_HOME
ENV R_HOME /usr/lib/R

# Chạy ứng dụng
CMD ["python", "app.py"]

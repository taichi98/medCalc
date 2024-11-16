# Sử dụng image cơ bản của Python
FROM python:3.10-slim

# Cài đặt các công cụ cơ bản
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt các gói Python từ requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy mã nguồn vào container
COPY . .

# Đặt biến môi trường cho Flask (chỉ định ứng dụng cần chạy)
ENV FLASK_APP=app.py
# Mở cổng cần thiết (theo mặc định Flask chạy trên cổng 5000)
EXPOSE 5000
# Lệnh để chạy ứng dụng
CMD ["flask", "run", "--host=0.0.0.0"]

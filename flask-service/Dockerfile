FROM python:3.10-slim

# Cài đặt các công cụ cơ bản
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install plotly
RUN pip install openpyxl
RUN pip install scipy

# Cài đặt các gói Python từ requirements.txt
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

# Đặt biến môi trường cho Flask (chỉ định ứng dụng cần chạy)
ENV FLASK_APP=app.py
EXPOSE 5000
# Lệnh để chạy ứng dụng
CMD ["flask", "run", "--host=0.0.0.0"]

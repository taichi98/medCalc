# Sử dụng một image Python có sẵn
FROM python:3.11-slim

# Cài đặt R và các thư viện cần thiết
RUN apt-get update && apt-get install -y \
    r-base \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt pip và rpy2
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy mã nguồn vào image
COPY . /app
WORKDIR /app

# Lệnh khởi động ứng dụng
CMD ["python", "app.py"]

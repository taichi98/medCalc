# Tầng cơ bản cho Python
FROM python:3.10-slim AS python-base

# Cài đặt công cụ cơ bản và các gói cần thiết cho Python
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

# Copy mã nguồn Python
COPY . /app

# Cài đặt Flask trong PATH toàn cục để tránh lỗi "can't find command"
RUN pip install flask gunicorn

# Tầng cơ bản cho PHP
FROM php:8.1-apache AS php-base

# Cài đặt các gói cần thiết cho PHP
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd

# Copy mã nguồn PHP
WORKDIR /var/www/html
COPY . /var/www/html

# Tầng cuối cùng để chạy đồng thời cả Python và PHP
FROM php:8.1-apache

# Sao chép từ cả hai tầng trước đó
COPY --from=python-base /app /app
COPY --from=php-base /var/www/html /var/www/html

# Cài đặt Supervisor để quản lý nhiều quy trình
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Cấu hình Supervisor để chạy cả Flask và Apache
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Đặt PATH cho Python để đảm bảo Flask được tìm thấy
ENV PATH="/usr/local/bin:$PATH"

# Mở các cổng cần thiết
EXPOSE 5000 80

# Lệnh khởi chạy Supervisor
CMD ["/usr/bin/supervisord", "-n"]

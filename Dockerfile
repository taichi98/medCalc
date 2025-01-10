# Tầng cơ bản cho Python
FROM python:3.10-slim AS python-base

# Cài đặt các công cụ và gói Python cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    libssl-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
RUN pip install flask plotly openpyxl scipy

# Copy mã nguồn Python
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /app

# Tầng cơ bản cho PHP
FROM php:8.1-fpm AS php-base

# Cài đặt PHP và các extension cần thiết
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd

# Copy mã nguồn PHP
WORKDIR /var/www/html
COPY . /var/www/html

# Tầng cuối cùng với Nginx làm reverse proxy
FROM nginx:alpine

# Copy cấu hình Nginx
COPY nginx.conf /etc/nginx/nginx.conf

# Copy các mã nguồn từ các tầng trước
COPY --from=python-base /app /app
COPY --from=php-base /var/www/html /var/www/html

# Mở các cổng cần thiết
EXPOSE 80

# Lệnh khởi động Nginx
CMD ["nginx", "-g", "daemon off;"]

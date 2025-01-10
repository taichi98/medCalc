FROM python:3.10-slim AS python-base

# Cài đặt các công cụ cơ bản cho Python
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
COPY . .

# Đặt biến môi trường cho Flask
ENV FLASK_APP=app.py

# Cổng Python chạy (Flask)
EXPOSE 5000


# Tầng PHP
FROM php:8.1-apache AS php-base

# Cài đặt các gói mở rộng cho PHP
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype=/usr/include/ --with-jpeg=/usr/include/ \
    && docker-php-ext-install gd

# Cài đặt Composer nếu cần
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# Copy mã nguồn PHP
WORKDIR /var/www/html
COPY . .

# Cổng PHP chạy (Apache)
EXPOSE 80

# Lựa chọn môi trường khi chạy container
CMD ["sh", "-c", "if [ \"$APP_ENV\" = 'python' ]; then flask run --host=0.0.0.0; else apache2-foreground; fi"]

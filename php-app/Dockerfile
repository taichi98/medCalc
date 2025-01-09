# Dockerfile cho PHP
FROM php:7.4-apache

# Cài đặt các tiện ích bổ sung (nếu cần)
RUN apt-get update && apt-get install -y libzip-dev \
    && docker-php-ext-install zip

# Sao chép mã nguồn PHP vào container
COPY ./php-app /var/www/html/

# Mở cổng 80 cho Apache
EXPOSE 80

# Sử dụng image cơ bản của Python
FROM python:3.11

# Cài đặt R và các thư viện cần thiết
RUN apt-get update && apt-get install -y r-base r-base-dev libcurl4-openssl-dev libssl-dev libxml2-dev

# Tạo script R để cài đặt gói `anthro`
RUN echo 'install.packages("devtools", repos="http://cran.rstudio.com/")' > /install_r_packages.R \
    && echo 'devtools::install_github("worldhealthorganization/anthro")' >> /install_r_packages.R

# Chạy script R để cài đặt các gói cần thiết
RUN Rscript /install_r_packages.R

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

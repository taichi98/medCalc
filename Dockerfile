# Sử dụng image Python làm base
FROM python:3.8-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Sao chép file requirements vào image
COPY requirements.txt .

# Cài đặt các phụ thuộc
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn vào image
COPY . .

# Expose cổng mà ứng dụng sẽ chạy
EXPOSE 5000

# Lệnh khởi động ứng dụng
CMD ["python", "app.py"]
 

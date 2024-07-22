# Gunakan base image Python 3.8 yang sudah termasuk pip
FROM python:3.8-slim

# Install dependensi sistem yang diperlukan untuk beberapa paket Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        libjpeg-dev \
        zlib1g-dev \
        libopencv-dev \
        libopenblas-dev \
        cmake \
        && rm -rf /var/lib/apt/lists/*

# Set working directory dalam container
WORKDIR /usr/src/app

# Install dependensi Python yang dibutuhkan
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi ke dalam container
COPY . .

# Expose port 5000 untuk akses web
EXPOSE 5000

# Command yang akan dijalankan saat container dijalankan
CMD ["python", "./compare.py"]

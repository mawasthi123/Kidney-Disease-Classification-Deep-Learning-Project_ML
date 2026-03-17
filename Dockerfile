# Use Bookworm; Buster is EOL and apt repos return 404
FROM python:3.10-slim-bookworm

# Build deps for h5py (pkg-config, HDF5) and any source builds (gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential pkg-config libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install --no-cache-dir --timeout 300 -r requirements.txt

CMD ["python3", "app.py"]
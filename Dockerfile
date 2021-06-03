FROM python:3.6
WORKDIR /monks-photo-filter
COPY monks_filter.py .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
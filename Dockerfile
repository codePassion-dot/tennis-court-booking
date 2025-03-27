# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/playwright/python:v1.51.0-noble
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install chrome --with-deps
COPY . .
CMD ["python", "test_booking.py"]

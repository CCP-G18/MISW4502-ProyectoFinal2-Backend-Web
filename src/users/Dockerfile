FROM python:3.12-slim

ENV PYTHONUNBUFFERED True

EXPOSE 5000
WORKDIR /app
COPY . ./

RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    libpq-dev \
    libffi-dev \
    musl-dev \
    git \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "main:app"]
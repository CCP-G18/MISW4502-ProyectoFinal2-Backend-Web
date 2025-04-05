FROM python:3.12-bullseye

ENV PYTHONUNBUFFERED True

EXPOSE 5002

WORKDIR /app

COPY . ./

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/*

RUN apt-get update && apt-get install -y --no-install-recommends --fix-missing \
    gcc-10 \
    g++-10 \
    build-essential \
    libpq-dev \
    libffi-dev \
    musl-dev \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/* /tmp/*

RUN pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5002", "main:app"]
FROM python:3.12-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        libffi-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .

EXPOSE 5006
CMD ["gunicorn", "-w", "10", "-b", "0.0.0.0:5006", "--timeout", "600",  "main:app"]
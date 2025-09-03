FROM python:3.13.7-slim

WORKDIR /app
RUN rm -rf /var/lib/apt/lists/*
COPY requirments.txt .
RUN pip install --no-cache-dir -r requirments.txt
COPY . .
RUN chmod +x metric_collector.sh
RUN addgroup --gid 1000 appuser \
    && adduser --disabled-password --gecos "" --uid 1000 --ingroup appuser appuser \
    && chown -R appuser:appuser /app
USER appuser
EXPOSE 8080
CMD ["python3", "metric_server.py"]
import logging
import time
from prometheus_client import Gauge, start_http_server
import subprocess
from enum import Enum

#init the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

disk_usage = Gauge("disk_usage", "Disk Usage Metric in Kb")
memory_usage = Gauge("memory_usage", "Memory Usage Metric in Kb")

#consts and enum
SCRIPT_PATH = "metric_collector.sh"
SCRIPT_TIMEOUT = 15
METRIC_SEPARATOR = '='
PORT = 8080
METRICS_COLLECT_INTERVAL = 300
class MetricName(Enum):
    DISK = "disk"
    MEMORY = "memory"
    
def collect_metrics():
    try:
        result = subprocess.run(["bash", SCRIPT_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=SCRIPT_TIMEOUT)
        if result.returncode != 0:
            logger.error(f"script execution error: {result.stderr}")
            return None
        metrics = {}
        for line in result.stdout.strip().splitlines():
            if METRIC_SEPARATOR in line:
                key, value = line.split(METRIC_SEPARATOR,1)
                try:
                    metrics[key.strip()] = float(value.strip())
                except ValueError:
                    logger.warning(f"invalid value in the metric: {line}")
        return metrics
    except Exception as e:
        logger.error(f"Unexpected error during script execution: {e}")
        return None
                

def update_metrics_gauge(metrics):
    if not metrics:
        return
    if MetricName.DISK.value in metrics:
        disk_usage.set(metrics[MetricName.DISK.value])
    if MetricName.MEMORY.value in metrics:
        memory_usage.set(metrics[MetricName.MEMORY.value])

def main():
    start_http_server(PORT)
    while True:
        try:
            metrics = collect_metrics()
            update_metrics_gauge(metrics)
        except Exception as e:
            logger.error(f"Error while collection and set metrics: {e}")
        time.sleep(METRICS_COLLECT_INTERVAL)

if __name__ == "__main__":
    main()
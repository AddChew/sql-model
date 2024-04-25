import time
import psutil
import subprocess

from prometheus_client import start_http_server, Gauge


memoryGauge = Gauge('memory_usage', 'Usage of memory in bytes')
start_http_server(8000)

proc = subprocess.Popen("./start.sh")
parent = psutil.Process(proc.pid)

for child in parent.children(recursive = True):
    if child.name() == "loki-linux-amd64":
        loki_proc = child

while proc.poll() is None:
    memoryGauge.set(loki_proc.memory_info().rss)
    time.sleep(1)

proc.terminate()
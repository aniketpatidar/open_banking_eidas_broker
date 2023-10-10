import json
import multiprocessing
import os

workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")

cores = multiprocessing.cpu_count()
workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * cores
if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)

# Gunicorn config variables
loglevel = use_loglevel
workers = web_concurrency
keepalive = 120
errorlog = "-"
# Set timeout to a bigger value than underlying application's timeout
# to avoid workers from being killed before the application returns a response
timeout = 300

# For debugging and testing
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    # Additional, non-gunicorn variables
    "workers_per_core": workers_per_core,
    "timeout": timeout,
}
print(json.dumps(log_data))

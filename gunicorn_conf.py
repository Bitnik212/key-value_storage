from multiprocessing import cpu_count

work_dir = "/app"

# Socket Path
bind = "0.0.0.0:8000"

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = work_dir + '/access_log'

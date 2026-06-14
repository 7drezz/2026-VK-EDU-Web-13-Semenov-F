import multiprocessing
bind = "127.0.0.1:8001"
workers = 2
worker_class = "sync"
timeout = 30
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
loglevel = "info"
wsgi_app = "application.wsgi:application"
pythonpath = "."
proc_name = "askpupkin"
daemon = False

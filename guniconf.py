import multiprocessing

# Server Socket
bind = 'unix:/tmp/gunicorn_ics_gen.sock'
backlog = 2048

# Worker Processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 100
max_requests = 100
timeout = 30
keepalive = 3
debug = False
spew = False

# Logging
logfile = '/var/www/ics-generator/ics-generator.log'
loglevel = 'info'
logconfig = None

# Process Name
proc_name = 'gunicorn_ics_generator'

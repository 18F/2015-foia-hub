
workers = 2
daemon = True

pidfile = "gunicorn.pid"
accesslog = "log/gunicorn.log"

application_module = "foia_hub.wsgi:application"
#! /bin/bash

gunicorn -k gevent server:app -c guniconf.py
service nginx restart

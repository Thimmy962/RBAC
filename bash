#!/bin/bash

# Start a simple HTTP server in the background
python healthcheck.py &

# Start Celery
celery -A RBAC worker --loglevel=info
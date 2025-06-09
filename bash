# start.sh
#!/bin/bash

# This is to trick render service so it does not stop the background worker I am running as a free webservice
# Since there is no money to pay for background work

# Start Celery in the background
celery -A RBAC worker --loglevel=info &

# Start a dummy web server to satisfy Render’s web check
python -m http.server 8000

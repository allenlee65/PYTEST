#!/bin/bash
# filepath: /home/allenlee/Workspace/PYTEST/docker-entrypoint.sh

# Start Xvfb for headless browser testing
Xvfb :99 -screen 0 1920x1080x24 &

# Wait for Xvfb to start
sleep 2

# Execute the command passed to docker run
exec "$@"
#!/bin/bash
# Railway startup script that properly handles PORT environment variable
PORT=${PORT:-8000}
exec uvicorn api.simple_api:app --host 0.0.0.0 --port $PORT


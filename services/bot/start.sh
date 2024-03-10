#!/bin/bash

python3 /app/src/main.py &
cd /app/src && uvicorn http_server:app --host 0.0.0.0 --port 8989

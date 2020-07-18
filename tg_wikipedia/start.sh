#!/usr/bin/env sh

echo "----- Starting server -----"
exec gunicorn src.app:init_app --config gunicorn_config.py --worker-class aiohttp.GunicornWebWorker

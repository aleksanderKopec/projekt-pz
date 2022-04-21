#!/bin/bash
(uvicorn main:app --host 0.0.0.0 --port 80 --forwarded-allow-ips='*') &
nginx -g "daemon off;"
#!/bin/sh

alembic upgrade head
hypercorn src/main:app -b 0.0.0.0:3000 --reload  --access-logfile -  --graceful-timeout 5  
ga 
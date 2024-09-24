#!/bin/sh

alembic upgrade head
hypercorn src/main:app -b 0.0.0.0:8000 --reload 

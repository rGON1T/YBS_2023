#!/bin/bash

bin/alembic upgrade head

cd /app/app

../bin/uvicorn main:app --host=0.0.0.0 --port=8080

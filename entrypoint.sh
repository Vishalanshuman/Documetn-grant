#!/bin/sh

echo "Waiting for database..."

until python -c "
import socket
socket.create_connection(('db', 5432), timeout=2)
print('Database is ready')
" 2>/dev/null
do
    echo "Database not ready..."
    sleep 2
done

echo "Running migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
# !/bin/sh

# Exit immediately if a command exits with a non-zero status.  
set -e  

echo "Applying database migrations..."  
alembic upgrade head  

echo "Runnng Server"  
uvicorn app.main:app --host 0.0.0.0 --port 8000

exec "$@"

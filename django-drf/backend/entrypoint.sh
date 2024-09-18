# !/bin/sh

# Exit immediately if a command exits with a non-zero status.  
set -e  

echo "Applying database migrations..."  
python manage.py migrate --noinput   

echo "Collecting static files..."  
python manage.py collectstatic --noinput  

# Run the command passed to the container after the entrypoint  
exec gunicorn API.wsgi:application  --bind 0.0.0.0:8000 --log-level debug  

exec "$@"

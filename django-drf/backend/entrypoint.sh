# !/bin/sh

echo "Applying database migrations..."  
python manage.py migrate --noinput   

echo "Collecting static files..."  
python manage.py collectstatic --noinput  

echo "Running Gunicorn server.."  
exec gunicorn API.wsgi:application  --bind 0.0.0.0:8000 --log-level debug  

exec "$@"

pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic --no-input --clear

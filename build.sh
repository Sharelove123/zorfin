#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Automatically create a default admin user if one doesn't exist
python manage.py shell -c "import os; from apps.users.models import User; email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@admin.com'); password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123'); User.objects.filter(email=email).exists() or User.objects.create_superuser('admin', email, password, role='admin')"

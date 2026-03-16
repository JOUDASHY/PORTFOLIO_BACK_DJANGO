#!/bin/bash
# Production deployment script with UTF-8 template fix

set -e  # Exit on error

echo "======================================"
echo "🚀 Starting Deployment"
echo "======================================"

# 1. Git pull
echo "📦 Pulling latest code..."
git pull origin main

# 2. Install dependencies (if needed)
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# 3. Database migrations
echo "🗄️ Running migrations..."
python manage.py migrate --noinput

# 4. Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 5. Fix UTF-8 encoding in templates
echo "🔧 Fixing UTF-8 encoding in message templates..."
python manage.py fix_template_encoding

# 6. Restart server (adjust based on your setup)
echo "🔄 Restarting server..."
# Uncomment ONE of these based on your setup:

# For systemd:
# sudo systemctl restart gunicorn

# For Supervisor:
# sudo supervisorctl restart all

# For Docker:
# docker-compose restart

# For direct process:
# sudo pkill -f gunicorn
# sleep 2
# gunicorn back_django_portfolio_me.wsgi:application --bind 0.0.0.0:8000 &

echo "======================================"
echo "✅ Deployment Complete!"
echo "======================================"

# Optional: Test the fix
echo "🧪 Testing template encoding..."
python manage.py shell -c "
from core.models import MessageTemplate
t = MessageTemplate.objects.filter(language='fr', is_default=True).first()
if t and 'é' in t.body or '✅' in t.body:
    print('✅ UTF-8 encoding looks good!')
else:
    print('⚠️ Templates may still have encoding issues')
"

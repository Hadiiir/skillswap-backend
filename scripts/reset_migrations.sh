#!/bin/bash

echo "🔄 Resetting migrations..."

# Delete existing migrations (except __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "✅ Old migrations have been deleted"

# Create new migrations
echo "📝 Creating new migrations..."

python manage.py makemigrations accounts
python manage.py makemigrations skills  
python manage.py makemigrations points
python manage.py makemigrations payments
python manage.py makemigrations chat
python manage.py makemigrations reviews
python manage.py makemigrations notifications

echo "✅ New migrations have been created"

# Apply migrations
echo "🚀 Applying migrations..."
python manage.py migrate

echo "🎉 Completed successfully!"

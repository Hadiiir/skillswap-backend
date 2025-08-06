#!/bin/bash

echo "🔧 Fixing Django Migrations"
echo "=========================="

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
    echo "✅ Virtual environment activated"
fi

# Remove all migration files except __init__.py
echo "🗑️  Removing old migration files..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Remove migration directories and recreate them
for app in accounts skills points chat payments reviews notifications; do
    if [ -d "$app/migrations" ]; then
        rm -rf "$app/migrations"
        mkdir -p "$app/migrations"
        touch "$app/migrations/__init__.py"
        echo "✅ Reset migrations for $app"
    fi
done

# Drop and recreate database
echo "🗄️  Resetting database..."
python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()
cursor.execute('DROP SCHEMA public CASCADE;')
cursor.execute('CREATE SCHEMA public;')
cursor.execute('GRANT ALL ON SCHEMA public TO postgres;')
cursor.execute('GRANT ALL ON SCHEMA public TO public;')
print('✅ Database reset completed')
"

# Create fresh migrations
echo "📝 Creating fresh migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations skills  
python manage.py makemigrations points
python manage.py makemigrations chat
python manage.py makemigrations payments
python manage.py makemigrations reviews
python manage.py makemigrations notifications

# Apply migrations
echo "⚡ Applying migrations..."
python manage.py migrate

echo "✅ Migrations fixed successfully!"
echo "🚀 You can now run the server: python manage.py runserver"

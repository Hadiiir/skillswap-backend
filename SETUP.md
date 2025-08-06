# SkillSwap Setup Guide

This guide will help you set up the SkillSwap backend for development.

## Quick Start Options

### Option 1: Local Development (Recommended for development)

This option uses SQLite and runs Django directly on your machine.

\`\`\`bash
# 1. Clone and navigate to the project
cd skillswap-backend

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run setup script
python scripts/setup_local_dev.py

# 5. Start development server
bash scripts/run_local.sh
\`\`\`

### Option 2: Docker Development

This option uses PostgreSQL and Redis in Docker containers.

\`\`\`bash
# 1. Make sure Docker is installed and running

# 2. Run setup script
bash scripts/setup_docker.sh

# 3. Access the application
# Main app: http://localhost:8000/
# Admin: http://localhost:8000/admin/
\`\`\`

## Default Credentials

- **Admin User**: admin@skillswap.com / admin123
- **Sample Users**: 
  - john@example.com / password123
  - sarah@example.com / password123
  - ahmed@example.com / password123

## API Endpoints

Once running, you can access:

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/ (browsable API)

### Key API Endpoints:

- `GET /api/skills/` - List all skills
- `GET /api/skills/?category=Programming` - Filter by category
- `GET /api/skills/?search=python` - Search skills
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `GET /api/users/profile/` - Get user profile

## Development Commands

### Local Development
\`\`\`bash
# Run server
python manage.py runserver --settings=skillswap.settings_local


# Create migrations
python manage.py makemigrations --settings=skillswap.settings_local

# Run migrations
python manage.py migrate --settings=skillswap.settings_local

# Create superuser
python manage.py createsuperuser --settings=skillswap.settings_local
\`\`\`

### Docker Development
\`\`\`bash
# View logs
docker-compose logs -f

# Run server
http://localhost:8000/admin/oauth2_provider/idtoken/

http://localhost:8000/api/skills/

http://localhost:8000/admin/


\`\`\`
### Testing
docker-compose up --build
docker-compose up -d
docker-compose ps
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
\`\`\`
### Testing
python scripts/create_superuser.py


# Run Django commands
docker-compose exec web python manage.py <command>

# Access database
docker-compose exec db psql -U skillswap -d skillswap

# Restart services
docker-compose restart
\`\`\`

## Troubleshooting

### Database Connection Issues
If you see "could not translate host name 'db'", you're trying to run Django outside Docker with Docker database settings. Use local development setup instead.

### Migration Issues
\`\`\`bash
# Reset migrations (local)
rm db.sqlite3
rm */migrations/0*.py
python manage.py makemigrations --settings=skillswap.settings_local
python manage.py migrate --settings=skillswap.settings_local

# Reset migrations (Docker)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
\`\`\`

### Port Conflicts
If ports 8000, 5432, or 6379 are in use:
1. Stop conflicting services
2. Or modify ports in docker-compose.yml

## Project Structure

\`\`\`
skillswap-backend/
├── accounts/          # User management
├── skills/           # Skills marketplace
├── points/           # Points system
├── chat/             # Real-time chat
├── payments/         # Payment processing
├── reviews/          # Review system
├── notifications/    # Notification system
├── scripts/          # Setup and utility scripts
└── skillswap/        # Main Django project
\`\`\`

## Next Steps

1. **Frontend Development**: Create React/Vue frontend
2. **API Integration**: Connect frontend to backend APIs
3. **Payment Setup**: Configure Stripe/Paymob keys
4. **Email Setup**: Configure SMTP settings
5. **Production Deploy**: Set up production environment

## Support

If you encounter issues:
1. Check this README
2. Review error logs
3. Ensure all dependencies are installed
4. Verify database connections

## run full project (Backend - frontend)
cd ~/skillswap-backend
source venv/bin/activate
python manage.py runserver



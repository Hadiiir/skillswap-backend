📘 SkillSwap Backend Documentation
A professional-grade Django REST API for SkillSwap: a platform enabling users to trade skills using a points-based system.

🚀 Features
🎯 Core Functionalities
User Management: Registration, JWT/OAuth authentication, profile management


Skill Marketplace: Create, search, and browse skills across multiple categories


Points System: Earn and spend points during skill exchanges


Order Management: Full order lifecycle handling


Real-time Chat: WebSocket-based private messaging


Payment Integration: Stripe, PayPal, Paymob support


Review System: Users can rate and review each transaction


Multi-language Support: Arabic & English (i18n-ready)



What is SkillSwap?
SkillSwap is a comprehensive skills exchange platform that allows users to:
Share knowledge


Learn new skills


Earn points through teaching others


All within a secure, structured, and multi-language environment.

❗ The Problem
Despite the rise of e-learning platforms, many issues remain:
High fees


No peer-to-peer learning


Lack of Arabic/localized support


No real-time communication


Trust & verification problems


No platform offering points-based skill trade




🎯 Problem Goal
To build a peer-to-peer skill exchange platform where:
Users trade skills using virtual points


Orders, payments, ratings, and messages are all managed securely


Arabic & English supported


Real-time messaging, notifications, and transactions


Admins can manage the system with a full dashboard



✅ What SkillSwap Solves
Peer-to-peer skill sharing through points


WebSocket-based real-time chat


Full Arabic & English support


Rating, reviews, and user verification


Multi-gateway payments (Stripe, PayPal, Paymob)


Points-based monetization for skills



✨ Key Features

🧑‍💼 User Management: JWT auth, OAuth2, profile & verification


🎯 Skills Marketplace: Add/browse skills, filter by category, Arabic/English


📦 Order Management: Order lifecycle (request → accept → complete)


🔔 Notifications: WebSocket-based + Celery, email + push


💬 Real-time Chat System: ChatRoom & Message models, linked to orders


💳 Payments: Stripe, PayPal, Paymob integration


⭐ Reviews: Rate users, auto-calculate averages


📖 API Docs: Swagger/OpenAPI, ReDoc


🛠 Admin Dashboard: Manage users, skills, payments




⚙️ Challenges & Solutions
Real-Time Communication: Used Django Channels + Redis


Secure Authentication: JWT + Django Allauth + OAuth2


Payment System: Modular service for Stripe, PayPal, Paymob


Multi-language Support: Arabic/English with translatable fields


Notification System: Celery-based email/push notification architecture


Points Economy: Credit/debit transaction history with user balances


You can view the Presentation project here:
https://www.canva.com/design/DAGvMZLQaOo/EE2q-cCgYENUyZyfZZN3vA/view?utm_content=DAGvMZLQaOo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h51c0f05736

Project repository:
https://github.com/Hadiiir/skillswap-backend.git

Project Doc:
https://docs.google.com/document/d/1781ZnTuYdQ0SKNJnPY2qSavwd6dbImpYdW-uF04_KC4/edit?tab=t.0



⚙️ Technical Features
RESTful API with DRF


PostgreSQL with performance optimization


Redis for caching


Celery for background tasks


WebSocket via Django Channels


Secure token-based auth (JWT)


Docker-ready deployment


Full test coverage (unit/integration)



🛠 Tech Stack
Category
Technology
Backend
Django 4.2 + Django REST Framework
Database
PostgreSQL
Caching
Redis
Real-time
Django Channels + WebSockets
Tasks
Celery + Redis Broker
Auth
JWT + Google OAuth2
Payments
Stripe, PayPal, Paymob
Deployment
Docker + Docker Compose
Storage
Local + AWS S3 (optional)


📋 Prerequisites
Python 3.11+


PostgreSQL 13+


Redis 6+


Docker & Docker Compose (recommended)



⚡ Quick Start
Option 1: Docker (Recommended)
git clone https://github.com/Hadiiir/skillswap-backend.git
cd skillswap-backend
cp .env.example .env  # then configure it

# Start the services
docker-compose up -d

# Run migrations and seed data
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell < scripts/seed_data.py

# Create superuser
docker-compose exec web python manage.py createsuperuser

Option 2: Manual Setup
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure .env and start services
createdb skillswap
python manage.py migrate
redis-server
python manage.py runserver

# Start celery worker
celery -A skillswap worker -l info


🧱 Database Schema (ERD)
+--------------------+          +--------------------+           +------------------------+
|       User         |◄────────►|      Skill         |◄─────────►|     SkillCategory      |
+--------------------+          +--------------------+           +------------------------+
| id (PK)            |          | id (PK)            |           | id (PK)                |
| username           |          | title              |           | name                   |
| email              |          | description        |           +------------------------+
| password           |          | price_in_points    |
| points             |          | user_id (FK)       |
| rating             |          | category_id (FK)   |
+--------------------+          +--------------------+

       ▲                             ▲
       │                             │
       │                             │
+--------------------+     +-------------------------+           +----------------------+
|     Review         |     |         Order           |◄─────────►|   PointsTransaction   |
+--------------------+     +-------------------------+           +----------------------+
| id (PK)            |     | id (PK)                 |           | id (PK)              |
| reviewer_id (FK)   |     | buyer_id (FK)           |           | user_id (FK)         |
| reviewee_id (FK)   |     | seller_id (FK)          |           | amount               |
| rating             |     | skill_id (FK)           |           | type ("credit/debit")|
| comment            |     | status                  |           | description          |
+--------------------+     | created_at              |           | created_at           |
                           +-------------------------+           +----------------------+

       ▲
       │
+---------------------+           +------------------------+
|     ChatRoom        |◄──────────►      Message           |
+---------------------+           +------------------------+
| id (PK)             |           | id (PK)                |
| user1_id (FK)       |           | chatroom_id (FK)       |
| user2_id (FK)       |           | sender_id (FK)         |
+---------------------+           | content                |
                                  | timestamp              |
                                  +------------------------+

+----------------------+
|      Payment         |
+----------------------+
| id (PK)              |
| user_id (FK)         |
| gateway ("Stripe"…)  |
| amount               |
| status               |
| transaction_id       |
| created_at           |
+----------------------+


📚 API Endpoints
🔐 Auth
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/refresh/
GET  /api/auth/profile/
PUT  /api/auth/profile/

🧠 Skills
GET    /api/skills/
POST   /api/skills/
GET    /api/skills/{id}/
PUT    /api/skills/{id}/
DELETE /api/skills/{id}/
GET    /api/skills/categories/

💰 Points & Orders
GET  /api/points/packages/
POST /api/points/purchase/
GET  /api/points/transactions/
POST /api/points/orders/
GET  /api/points/orders/
PUT  /api/points/orders/{id}/

💬 Chat
GET  /api/chat/rooms/
GET  /api/chat/rooms/{id}/
POST /api/chat/rooms/{id}/send/

💳 Payments
POST /api/payments/stripe/
POST /api/payments/paypal/
POST /api/payments/paymob/
GET  /api/payments/history/


🗄️ Database Schema
Key Models
User: Extended profile, points balance, ratings


Skill: Category, pricing, tags


Order: Buyer, seller, status, timestamps


PointsTransaction: Points history & balance


ChatRoom: Messages & participants


Review: Linked to orders


Payment: Transaction logs



⚙️ Configuration (ENV)
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=Ture
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# PostgreSQL
DATABASE_URL=postgresql://skillswap:skillswap123@localhost:5432/skillswap

# Redis
REDIS_URL=redis://localhost:6379/0

# Payment Keys
STRIPE_SECRET_KEY=...
PAYMOB_API_KEY=...

# Email
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=...
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=hadeer.gamal3010@gmail



🧪 Testing & Coverage
python manage.py test
coverage run --source='.' manage.py test
coverage report
coverage html


📈 Performance Optimization
PostgreSQL Indexing


Redis Caching


Query Optimization: select_related, prefetch_related


Background Processing: Celery


API Pagination



🔒 Security Best Practices
JWT Authentication


CORS Configuration


Input Validation


XSS/SQL Injection Protection (Django ORM)


Rate Limiting (to be added)



🚀 Deployment
Docker Production
docker-compose -f docker-compose.prod.yml up -d

Production Checklist ✅
DEBUG=False


ALLOWED_HOSTS configured


SSL (HTTPS)


Static/media setup


Logging & Monitoring


CI/CD Pipeline


Backups enabled



📊 Monitoring & Analytics
User & Skill statistics


Transaction volumes


Payment success rates


Performance metrics (requests, latency)



🎯 Future Roadmap
Mobile API optimization


Elasticsearch search


AI skill matching


Video call feature


Analytics dashboard


Multi-currency support


API versioning



📄 License
This project is licensed under the MIT License.

Built with ❤️ by Hadeer for the ProDev Backend Program – Project Nexus


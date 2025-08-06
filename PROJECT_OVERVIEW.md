# 🚀 SkillSwap Backend - Skill Exchange System

## 📋 Project Overview

SkillSwap is a fully integrated backend system for a skill exchange platform, built using Django and Django REST Framework. The system provides all the essential features needed to create an interactive platform for exchanging skills and services.

## 🎯 Key Features

### 👥 User Management (Accounts App)

* User registration and login
* Secure authentication using JWT
* Detailed user profiles with images
* Points and rating system
* Personal skill management

### 🎯 Skill Marketplace (Skills App)

* Browse and manage skills and services
* Flexible multi-categorization
* Advanced search and filtering
* Point-based pricing system
* Media gallery for each skill
* FAQs for each skill

### 💰 Points System (Points App)

* Manage user point balances
* Full transaction history
* Order and booking system
* Platform commission calculation
* Detailed financial reports

### 💬 Chat System (Chat App)

* Real-time user conversations
* WebSocket support for live updates
* File and media sharing
* Message history
* Instant notifications

### 💳 Payment System (Payments App)

* Integration with Stripe for international payments
* Integration with Paymob for local payments
* Secure payment processing
* Automatic invoice generation
* Track payment statuses

### ⭐ Review System (Reviews App)

* Rate skills and services
* Detailed user reviews
* Star rating system (1-5)
* Review statistics
* Filtering and sorting reviews

### 🔔 Notification System (Notifications App)

* Instant and scheduled notifications
* Email notifications
* Mobile push notifications
* Customizable notification types
* Track notification status

## 🛠️ Technologies Used

### Backend Framework

* **Django 4.2** – Main web framework
* **Django REST Framework** – For building APIs
* **Django Channels** – For real-time communications
* **Celery** – For background task processing

### Database

* **PostgreSQL** – Main production database
* **Redis** – For caching and sessions
* **SQLite** – For local development

### Authentication & Security

* **JWT (JSON Web Tokens)** – For authentication
* **OAuth2** – Integration with external services
* **Django AllAuth** – For social authentication

### Payments

* **Stripe API** – International payments
* **Paymob API** – Local payments

### DevOps

* **Docker & Docker Compose** – For containerization
* **WhiteNoise** – For serving static files
* **CORS Headers** – For frontend integration

## 📡 API Endpoints

### Authentication APIs

```
POST /api/auth/register/          # Register a new user
POST /api/auth/login/             # Login
POST /api/auth/logout/            # Logout
GET  /api/auth/profile/           # View profile
PUT  /api/auth/profile/           # Update profile
POST /api/auth/change-password/   # Change password
```

### Skills APIs

```
GET    /api/skills/               # List skills
POST   /api/skills/               # Create a new skill
GET    /api/skills/{id}/          # Skill details
PUT    /api/skills/{id}/          # Update a skill
DELETE /api/skills/{id}/          # Delete a skill
GET    /api/skills/categories/    # List categories
GET    /api/skills/search/        # Search skills
```

### Points APIs

```
GET  /api/points/balance/         # User point balance
POST /api/points/transfer/        # Transfer points
GET  /api/points/transactions/    # Transaction history
POST /api/points/purchase/        # Purchase points
```

### Chat APIs

```
GET  /api/chat/conversations/     # List conversations
POST /api/chat/conversations/     # Start a new conversation
GET  /api/chat/messages/{id}/     # Conversation messages
POST /api/chat/messages/          # Send a message
```

### Payments APIs

```
POST /api/payments/create/        # Create a payment
GET  /api/payments/history/       # Payment history
POST /api/payments/webhook/       # Payment webhook
GET  /api/payments/methods/       # Available payment methods
```

### Reviews APIs

```
POST /api/reviews/                # Create a review
GET  /api/reviews/skill/{id}/     # Reviews for a skill
GET  /api/reviews/user/{id}/      # Reviews for a user
PUT  /api/reviews/{id}/           # Update a review
DELETE /api/reviews/{id}/         # Delete a review
```

## 🚀 How to Run the Project

### Using Docker (Recommended)

```bash
# Run the project
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create a superuser
docker-compose exec web python manage.py createsuperuser

# Load sample data
docker-compose exec web python create_sample_data.py
```

### Local Development

```bash
# Setup local development environment
python scripts/setup_local_dev.py

# Run development server
python manage.py runserver --settings=skillswap.settings_local
```

## 🔧 Configuration & Setup

### Environment Variables

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/dbname
REDIS_URL=redis://localhost:6379/0
STRIPE_SECRET_KEY=sk_test_...
PAYMOB_API_KEY=your-paymob-key
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Database Configuration

* **Production**: PostgreSQL
* **Development**: SQLite
* **Cache**: Redis
* **Sessions**: Redis

## 📊 Project Statistics

* **8 Django Apps** – Well-organized modular apps
* **15+ Models** – Rich database schema
* **25+ API Endpoints** – Comprehensive REST APIs
* **Real-time Features** – Built with WebSocket
* **Multi-language Support** – Arabic & English
* **Advanced Security** – JWT & OAuth2 authentication

## 🎨 Advanced Features

### Smart Recommendation System

* Personalized recommendations
* User behavior analytics
* Machine learning algorithms

### Advanced Search Engine

* Full-text search
* Multi-criteria filtering
* Intelligent ranking

### Advanced Security System

* Protection from CSRF & XSS
* Sensitive data encryption
* Suspicious activity monitoring

### Performance Monitoring

* API performance tracking
* Usage statistics
* Error reporting and logging

## 🌐 Project Access

After launching the project, you can access:

* **Main Site**: [http://localhost:8000/](http://localhost:8000/)
* **Admin Panel**: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* **Main API**: [http://localhost:8000/api/](http://localhost:8000/api/)
* **WebSocket Chat**: ws\://localhost:8000/ws/chat/

### Default Login Credentials

* **Email**: [admin@skillswap.com](mailto:admin@skillswap.com)
* **Password**: admin123

## 🤝 Contributing to the Project

This project is open to contributions and improvements. You can contribute by:

* Adding new features
* Fixing bugs
* Improving performance
* Updating documentation

## 📞 Support & Help

For help or to report issues:

* Open an issue on GitHub
* Check the documentation
* Contact the development team

---

**This project was carefully crafted to be a complete and scalable backend system for a skill exchange platform.** 🚀
# SkillSwap Backend API

A comprehensive Django REST API for a skill exchange platform where users can trade skills using a points-based system.

## 🚀 Features

### Core Functionality
- **User Management**: Registration, authentication, profiles with JWT & OAuth
- **Skill Marketplace**: Create, browse, and search skills across categories
- **Points System**: Earn and spend points for skill exchanges
- **Order Management**: Complete order lifecycle from creation to completion
- **Real-time Chat**: WebSocket-based messaging between users
- **Payment Integration**: Multiple payment gateways (Stripe, PayPal, Paymob)
- **Review System**: Rate and review completed transactions
- **Multi-language Support**: Arabic and English localization

### Technical Features
- **RESTful API**: Well-structured endpoints following REST principles
- **Database Optimization**: Proper indexing and query optimization
- **Caching**: Redis-based caching for improved performance
- **Background Tasks**: Celery for asynchronous task processing
- **Real-time Features**: WebSocket support for live chat
- **Security**: JWT authentication, CORS handling, input validation
- **Documentation**: Comprehensive API documentation
- **Testing**: Unit and integration tests
- **Deployment Ready**: Docker containerization and production settings

## 🛠 Tech Stack

- **Framework**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL with optimized indexes
- **Cache**: Redis for caching and session storage
- **Real-time**: Django Channels with WebSocket support
- **Background Tasks**: Celery with Redis broker
- **Authentication**: JWT + OAuth2 (Google)
- **Payments**: Stripe, PayPal, Paymob integration
- **File Storage**: Local storage with AWS S3 support
- **Deployment**: Docker + Docker Compose

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
\`\`\`bash
git clone https://github.com/Hadiiir/skillswap-backend.git
cd skillswap-backend
\`\`\`

2. **Set up environment variables**
\`\`\`bash
cp .env.example .env
# Edit .env with your configuration
\`\`\`

3. **Start services**
\`\`\`bash
docker-compose up -d
\`\`\`

4. **Run migrations and seed data**
\`\`\`bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py shell < scripts/seed_data.py
\`\`\`

5. **Create superuser**
\`\`\`bash
docker-compose exec web python manage.py createsuperuser
\`\`\`

### Manual Installation

1. **Create virtual environment**
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

2. **Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Set up database**
\`\`\`bash
createdb skillswap
python manage.py migrate
\`\`\`

4. **Start Redis**
\`\`\`bash
redis-server
\`\`\`

5. **Run development server**
\`\`\`bash
python manage.py runserver
\`\`\`

6. **Start Celery worker (in another terminal)**
\`\`\`bash
celery -A skillswap worker -l info
\`\`\`

## 📚 API Documentation

### Authentication Endpoints

\`\`\`
POST /api/auth/register/          # User registration
POST /api/auth/login/             # User login
POST /api/auth/logout/            # User logout
POST /api/auth/refresh/           # Refresh JWT token
GET  /api/auth/profile/           # Get user profile
PUT  /api/auth/profile/           # Update user profile
\`\`\`

### Skills Endpoints

\`\`\`
GET    /api/skills/               # List all skills
POST   /api/skills/               # Create new skill
GET    /api/skills/{id}/          # Get skill details
PUT    /api/skills/{id}/          # Update skill
DELETE /api/skills/{id}/          # Delete skill
GET    /api/skills/categories/    # List categories
\`\`\`

### Points & Orders Endpoints

\`\`\`
GET  /api/points/packages/        # List points packages
POST /api/points/purchase/        # Purchase points
GET  /api/points/transactions/    # Transaction history
POST /api/points/orders/          # Create order
GET  /api/points/orders/          # List user orders
PUT  /api/points/orders/{id}/     # Update order status
\`\`\`

### Chat Endpoints

\`\`\`
GET  /api/chat/rooms/             # List chat rooms
GET  /api/chat/rooms/{id}/        # Get chat messages
POST /api/chat/rooms/{id}/send/   # Send message
\`\`\`

### Payment Endpoints

\`\`\`
POST /api/payments/stripe/        # Process Stripe payment
POST /api/payments/paypal/        # Process PayPal payment
POST /api/payments/paymob/        # Process Paymob payment
GET  /api/payments/history/       # Payment history
\`\`\`

## 🏗 Database Schema

### Key Models

- **User**: Extended Django user with points, rating, and preferences
- **Skill**: Services offered by users with pricing and details
- **Order**: Transaction records between buyers and sellers
- **PointsTransaction**: All points movements and balances
- **ChatRoom**: Real-time messaging between users
- **Review**: Rating and feedback system
- **Payment**: Payment processing records

## 🔧 Configuration

### Environment Variables

\`\`\`env
# Core Django Settings
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# Redis
REDIS_URL=redis://localhost:6379/0

# Payment Gateways
STRIPE_SECRET_KEY=sk_live_...
PAYMOB_API_KEY=your-paymob-key

# Email
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your-app-password
\`\`\`

## 🧪 Testing

Run the test suite:

\`\`\`bash
python manage.py test
\`\`\`

Run with coverage:

\`\`\`bash
coverage run --source='.' manage.py test
coverage report
coverage html
\`\`\`


## 🧪 Testing

Run `python manage.py test` to execute all tests.

docker-compose -f docker-compose.simple.yml up -d && sleep 15 && curl http://localhost:8000/api/skills/


## 📊 Performance Features

- **Database Indexing**: Optimized queries with proper indexes
- **Caching Strategy**: Redis caching for frequently accessed data
- **Query Optimization**: Select_related and prefetch_related usage
- **Pagination**: Efficient pagination for large datasets
- **Background Processing**: Celery for heavy operations

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **CORS Configuration**: Proper cross-origin resource sharing
- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Prevention**: Built-in Django security features
- **Rate Limiting**: API rate limiting (can be added)

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL certificates
- [ ] Configure static file serving
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

### Docker Production

\`\`\`bash
docker-compose -f docker-compose.prod.yml up -d
\`\`\`

## 📈 Monitoring & Analytics

The API includes built-in analytics for:
- User registration and activity
- Skill performance metrics
- Transaction volumes
- Payment success rates
- System performance metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API endpoints

## 🎯 Future Enhancements

- [ ] Mobile app API optimization
- [ ] Advanced search with Elasticsearch
- [ ] Machine learning recommendations
- [ ] Video call integration
- [ ] Advanced analytics dashboard
- [ ] Multi-currency support
- [ ] Affiliate program
- [ ] API versioning

---

**Built with ❤️ for the ProDev Backend Program - Project Nexus**

This backend API demonstrates professional-level Django development with industry best practices, scalable architecture, and comprehensive feature set suitable for a production skill-sharing platform.




# SkillSwap Frontend

A modern React TypeScript application for the SkillSwap platform - where users can learn, teach, and exchange skills.

## 🚀 Features

- **Modern UI/UX** - Built with React 18 and TypeScript
- **Responsive Design** - Works perfectly on all devices
- **Authentication** - JWT-based authentication with auto-refresh
- **Real-time Chat** - WebSocket integration for messaging
- **Points System** - Integrated points management
- **Skills Management** - Browse, create, and manage skills
- **Payment Integration** - Multiple payment gateways support

## 🛠️ Tech Stack

- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **React Router** for navigation
- **Axios** for API communication
- **React Toastify** for notifications
- **Heroicons** for icons

## 📦 Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd skillswap-frontend
\`\`\`

2. Install dependencies:
\`\`\`bash
npm install
\`\`\`

3. Create environment file:
\`\`\`bash
cp .env.example .env
\`\`\`

4. Update environment variables in `.env`:
\`\`\`env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WEBSOCKET_URL=ws://localhost:8000/ws
\`\`\`

5. Start the development server:
\`\`\`bash
npm start
\`\`\`

## 🏗️ Project Structure

\`\`\`
src/
├── components/          # Reusable components
│   ├── Auth/           # Authentication components
│   └── Layout/         # Layout components
├── contexts/           # React contexts
├── pages/              # Page components
│   ├── Auth/           # Authentication pages
│   ├── Skills/         # Skills-related pages
│   ├── Dashboard/      # Dashboard pages
│   └── ...
├── services/           # API services
├── types/              # TypeScript type definitions
└── utils/              # Utility functions
\`\`\`

## 🔧 Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## 🌐 API Integration

The frontend integrates with the SkillSwap backend API endpoints:

### Authentication
- POST `/api/auth/register/` - User registration
- POST `/api/auth/login/` - User login
- POST `/api/auth/logout/` - User logout
- GET `/api/auth/profile/` - Get user profile

### Skills
- GET `/api/skills/` - List all skills
- POST `/api/skills/` - Create new skill
- GET `/api/skills/{id}/` - Get skill details

### Points & Orders
- GET `/api/points/packages/` - List points packages
- POST `/api/points/purchase/` - Purchase points
- POST `/api/points/orders/` - Create order

### Chat
- GET `/api/chat/rooms/` - List chat rooms
- POST `/api/chat/rooms/{id}/send/` - Send message

### Payments
- POST `/api/payments/stripe/` - Process Stripe payment
- POST `/api/payments/paypal/` - Process PayPal payment

## 🎨 Styling

The project uses Tailwind CSS with a custom design system:

- **Primary Colors**: Blue shades for main UI elements
- **Secondary Colors**: Purple shades for accents
- **Typography**: Inter font family
- **Components**: Custom button and form styles

## 🔐 Authentication

The app uses JWT-based authentication with:

- Access token for API requests
- Refresh token for automatic token renewal
- Protected routes for authenticated users
- Automatic logout on token expiration

## 📱 Responsive Design

The application is fully responsive and works on:

- Desktop (1024px+)
- Tablet (768px - 1023px)
- Mobile (320px - 767px)

## 🚀 Deployment

1. Build the project:
\`\`\`bash
npm run build
\`\`\`

2. Deploy the `build` folder to your hosting service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

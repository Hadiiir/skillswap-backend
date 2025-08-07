#!/bin/bash

# 🚀 SkillSwap Server Deployment Script
# This script deploys SkillSwap to a remote server

set -e

echo "🚀 SkillSwap Server Deployment"
echo "=============================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Configuration
SERVER_USER=${SERVER_USER:-"root"}
SERVER_HOST=${SERVER_HOST:-"your-server-ip"}
PROJECT_DIR=${PROJECT_DIR:-"/opt/skillswap"}
DOMAIN_NAME=${DOMAIN_NAME:-"yourdomain.com"}
USER=${SERVER_USER:-ubuntu}

# Check if server details are provided
if [ "$SERVER_HOST" = "your-server-ip" ]; then
    print_error "Please set SERVER_HOST environment variable"
    echo "Usage: SERVER_HOST=1.2.3.4 SERVER_USER=ubuntu ./scripts/deploy_to_server.sh"
    exit 1
fi

print_status "Deploying to server: $SERVER_USER@$SERVER_HOST"
print_status "Project directory: $PROJECT_DIR"
print_status "Domain: $DOMAIN_NAME"

# Create deployment script
cat > /tmp/deploy_skillswap.sh << 'DEPLOY_SCRIPT'
#!/bin/bash
set -e

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker $USER
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Install Nginx
apt-get install -y nginx certbot python3-certbot-nginx

# Create project directory
mkdir -p PROJECT_DIR_PLACEHOLDER
cd PROJECT_DIR_PLACEHOLDER

# Clone or update repository (if using Git)
# git clone https://github.com/yourusername/skillswap-backend.git .
# or copy files from local

echo "Server setup completed!"
DEPLOY_SCRIPT

# Replace placeholder
sed -i "s|PROJECT_DIR_PLACEHOLDER|$PROJECT_DIR|g" /tmp/deploy_skillswap.sh

# Copy deployment script to server
print_status "Copying deployment script to server..."
scp /tmp/deploy_skillswap.sh $SERVER_USER@$SERVER_HOST:/tmp/

# Run deployment script on server
print_status "Running deployment script on server..."
ssh $SERVER_USER@$SERVER_HOST "chmod +x /tmp/deploy_skillswap.sh && /tmp/deploy_skillswap.sh"

# Copy project files to server
print_status "Copying project files to server..."
rsync -avz --exclude='*.pyc' --exclude='__pycache__' --exclude='.git' --exclude='logs' --exclude='media' . $SERVER_USER@$SERVER_HOST:$PROJECT_DIR/

# Create production environment on server
print_status "Setting up production environment..."
ssh $SERVER_USER@$SERVER_HOST << EOF
cd $PROJECT_DIR

# Update environment file with server-specific values
sed -i "s|yourdomain.com|$DOMAIN_NAME|g" .env.production
sed -i "s|localhost,127.0.0.1|localhost,127.0.0.1,$DOMAIN_NAME,www.$DOMAIN_NAME|g" .env.production

# Make scripts executable
chmod +x scripts/*.sh

# Run production deployment
./scripts/production_deploy.sh

# Setup SSL certificate
if [ "$DOMAIN_NAME" != "yourdomain.com" ]; then
    certbot --nginx -d $DOMAIN_NAME -d www.$DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
fi

# Setup firewall
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

echo "Deployment completed successfully!"
EOF

print_success "Deployment completed!"
echo
echo "🌐 Your SkillSwap application is now live!"
echo "=================================="
echo "🔗 URLs:"
echo "   • Website: https://$DOMAIN_NAME"
echo "   • API: https://$DOMAIN_NAME/api/"
echo "   • Admin: https://$DOMAIN_NAME/admin/"
echo "   • Swagger: https://$DOMAIN_NAME/swagger/"
echo
echo "👨‍💼 Admin Credentials:"
echo "   • Email: admin@skillswap.com"
echo "   • Password: admin123"
echo
echo "📋 Next Steps:"
echo "   1. Update DNS records to point to $SERVER_HOST"
echo "   2. Change default passwords"
echo "   3. Configure email settings"
echo "   4. Set up monitoring and backups"
echo
print_warning "Remember to secure your server and change default credentials!"

# Cleanup
rm /tmp/deploy_skillswap.sh

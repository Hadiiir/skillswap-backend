#!/bin/bash

echo "🐚 SkillSwap Shell Access"
echo "========================"

if [ "$1" ]; then
    SERVICE=$1
else
    SERVICE="web"
fi

echo "🔗 Connecting to $SERVICE container..."

case $SERVICE in
    "web"|"django")
        docker-compose exec web bash
        ;;
    "db"|"postgres")
        docker-compose exec db psql -U skillswap_user -d skillswap
        ;;
    "redis")
        docker-compose exec redis redis-cli
        ;;
    "celery")
        docker-compose exec celery bash
        ;;
    *)
        echo "❌ Unknown service: $SERVICE"
        echo "Available services: web, db, redis, celery"
        exit 1
        ;;
esac

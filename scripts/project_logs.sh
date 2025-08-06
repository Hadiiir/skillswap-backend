#!/bin/bash

# Script to view logs for different services

SERVICE=${1:-"all"}

case $SERVICE in
    "web")
        echo "📋 Web Service Logs:"
        docker-compose logs -f web
        ;;
    "db")
        echo "📋 Database Logs:"
        docker-compose logs -f db
        ;;
    "redis")
        echo "📋 Redis Logs:"
        docker-compose logs -f redis
        ;;
    "celery")
        echo "📋 Celery Worker Logs:"
        docker-compose logs -f celery
        ;;
    "beat")
        echo "📋 Celery Beat Logs:"
        docker-compose logs -f celery-beat
        ;;
    "all"|*)
        echo "📋 All Services Logs:"
        docker-compose logs -f
        ;;
esac

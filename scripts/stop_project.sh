#!/bin/bash

echo "🛑 Stopping the SkillSwap Project"
echo "========================"

# Stop all containers
docker-compose -f docker-compose.simple.yml down

echo "✅ All services have been stopped"

# Show container status
echo "📊 Container status:"
docker-compose -f docker-compose.simple.yml ps

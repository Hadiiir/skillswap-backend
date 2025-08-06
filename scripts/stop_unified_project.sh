#!/bin/bash

echo "🛑 Stopping SkillSwap Unified Project..."

docker-compose down

docker-compose down --remove-orphans

echo "✅ SkillSwap Unified Project stopped!"

#!/bin/bash

echo "🔄 Restarting SkillSwap Unified Project..."

# Stop Project
./scripts/stop_unified_project.sh

# Start Project
./scripts/start_unified_project.sh

echo "✅ SkillSwap Unified Project restarted!"

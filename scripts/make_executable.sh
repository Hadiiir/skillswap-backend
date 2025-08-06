#!/bin/bash

# Make all scripts executable
chmod +x scripts/*.sh

echo "✅ All scripts are now executable!"
echo ""
echo "Available commands:"
echo "  ./scripts/start_complete_project.sh  - Start the complete project"
echo "  ./scripts/stop_complete_project.sh   - Stop the project"
echo "  ./scripts/project_status.sh          - Check project status"
echo "  ./scripts/project_logs.sh [service]  - View logs (web/db/redis/celery/all)"

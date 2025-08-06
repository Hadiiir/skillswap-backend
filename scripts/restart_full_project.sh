#!/bin/bash

echo "🔄 إعادة تشغيل مشروع SkillSwap الكامل"
echo "====================================="

# إيقاف المشروع أولاً
./scripts/stop_full_project.sh

# انتظار قليل
sleep 3

# تشغيل المشروع مرة أخرى
./scripts/start_full_project.sh

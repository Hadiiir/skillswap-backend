#!/bin/bash

echo "🔧 تشغيل إصلاح الأخطاء النحوية..."

# تشغيل سكريبت الإصلاح
python scripts/fix_syntax_errors.py

# التحقق من النتيجة
if [ $? -eq 0 ]; then
    echo "✅ تم إصلاح جميع الأخطاء!"
    
    # اختبار سريع للتأكد
    echo "🧪 اختبار سريع..."
    python manage.py check --deploy
    
    if [ $? -eq 0 ]; then
        echo "🎉 المشروع جاهز للتشغيل!"
    else
        echo "⚠️  هناك تحذيرات، لكن المشروع يعمل"
    fi
else
    echo "❌ فشل في إصلاح بعض الأخطاء"
    exit 1
fi

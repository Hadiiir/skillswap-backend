#!/usr/bin/env python
"""
Categories Seeder for SkillSwap
Seeds skill categories with comprehensive data matching the Category model
"""
import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from skills.models import Category

class CategoriesSeeder(BaseSeeder):
    """Seeder for skill categories matching the Category model exactly"""
    
    def get_data(self):
        """Return categories data matching Category model fields"""
        return [
            {
                'name': 'البرمجة وتطوير الويب',
                'name_ar': 'البرمجة وتطوير الويب',
                'description': 'تعلم لغات البرمجة المختلفة وتطوير المواقع والتطبيقات باستخدام أحدث التقنيات والأدوات',
                'description_ar': 'تعلم لغات البرمجة المختلفة وتطوير المواقع والتطبيقات باستخدام أحدث التقنيات والأدوات',
                'icon': 'fas fa-code',
                'is_active': True
            },
            {
                'name': 'التصميم الجرافيكي والإبداعي',
                'name_ar': 'التصميم الجرافيكي والإبداعي',
                'description': 'تصميم الشعارات والهويات البصرية والمواد التسويقية والإعلانية باستخدام أدوات التصميم المتقدمة',
                'description_ar': 'تصميم الشعارات والهويات البصرية والمواد التسويقية والإعلانية باستخدام أدوات التصميم المتقدمة',
                'icon': 'fas fa-palette',
                'is_active': True
            },
            {
                'name': 'التسويق الرقمي والإلكتروني',
                'name_ar': 'التسويق الرقمي والإلكتروني',
                'description': 'استراتيجيات التسويق عبر الإنترنت ووسائل التواصل الاجتماعي وتحسين محركات البحث',
                'description_ar': 'استراتيجيات التسويق عبر الإنترنت ووسائل التواصل الاجتماعي وتحسين محركات البحث',
                'icon': 'fas fa-bullhorn',
                'is_active': True
            },
            {
                'name': 'الكتابة والترجمة والتحرير',
                'name_ar': 'الكتابة والترجمة والتحرير',
                'description': 'كتابة المحتوى الإبداعي والتسويقي والترجمة بين اللغات المختلفة والتحرير اللغوي',
                'description_ar': 'كتابة المحتوى الإبداعي والتسويقي والترجمة بين اللغات المختلفة والتحرير اللغوي',
                'icon': 'fas fa-pen',
                'is_active': True
            },
            {
                'name': 'الأعمال والاستشارات المهنية',
                'name_ar': 'الأعمال والاستشارات المهنية',
                'description': 'استشارات الأعمال وإدارة المشاريع والتخطيط الاستراتيجي وريادة الأعمال',
                'description_ar': 'استشارات الأعمال وإدارة المشاريع والتخطيط الاستراتيجي وريادة الأعمال',
                'icon': 'fas fa-briefcase',
                'is_active': True
            },
            {
                'name': 'التعليم والتدريب المهني',
                'name_ar': 'التعليم والتدريب المهني',
                'description': 'التدريس والتدريب في مختلف المجالات وإنشاء المحتوى التعليمي والدورات التدريبية',
                'description_ar': 'التدريس والتدريب في مختلف المجالات وإنشاء المحتوى التعليمي والدورات التدريبية',
                'icon': 'fas fa-graduation-cap',
                'is_active': True
            },
            {
                'name': 'تحليل البيانات والذكاء الاصطناعي',
                'name_ar': 'تحليل البيانات والذكاء الاصطناعي',
                'description': 'تحليل البيانات وعلوم البيانات والذكاء الاصطناعي وتعلم الآلة والتحليل الإحصائي',
                'description_ar': 'تحليل البيانات وعلوم البيانات والذكاء الاصطناعي وتعلم الآلة والتحليل الإحصائي',
                'icon': 'fas fa-chart-bar',
                'is_active': True
            },
            {
                'name': 'الفيديو والصوتيات والمونتاج',
                'name_ar': 'الفيديو والصوتيات والمونتاج',
                'description': 'تحرير الفيديو وإنتاج الصوت والرسوم المتحركة والمحتوى المتعدد الوسائط',
                'description_ar': 'تحرير الفيديو وإنتاج الصوت والرسوم المتحركة والمحتوى المتعدد الوسائط',
                'icon': 'fas fa-video',
                'is_active': True
            },
            {
                'name': 'التصوير الفوتوغرافي المحترف',
                'name_ar': 'التصوير الفوتوغرافي المحترف',
                'description': 'التصوير الفوتوغرافي للأشخاص والمنتجات والأحداث وتحرير الصور باحترافية',
                'description_ar': 'التصوير الفوتوغرافي للأشخاص والمنتجات والأحداث وتحرير الصور باحترافية',
                'icon': 'fas fa-camera',
                'is_active': True
            },
            {
                'name': 'الموسيقى والإنتاج الصوتي',
                'name_ar': 'الموسيقى والإنتاج الصوتي',
                'description': 'إنتاج الموسيقى وتصميم الصوت والتعليق الصوتي وهندسة الصوت والتسجيل',
                'description_ar': 'إنتاج الموسيقى وتصميم الصوت والتعليق الصوتي وهندسة الصوت والتسجيل',
                'icon': 'fas fa-music',
                'is_active': True
            },
            {
                'name': 'الصحة واللياقة البدنية',
                'name_ar': 'الصحة واللياقة البدنية',
                'description': 'التدريب الرياضي والاستشارات الصحية والتغذية واليوغا والعلاج الطبيعي',
                'description_ar': 'التدريب الرياضي والاستشارات الصحية والتغذية واليوغا والعلاج الطبيعي',
                'icon': 'fas fa-heartbeat',
                'is_active': True
            },
            {
                'name': 'الحرف اليدوية والفنون التقليدية',
                'name_ar': 'الحرف اليدوية والفنون التقليدية',
                'description': 'الأعمال اليدوية والحرف التقليدية والحديثة والفنون التشكيلية والنحت',
                'description_ar': 'الأعمال اليدوية والحرف التقليدية والحديثة والفنون التشكيلية والنحت',
                'icon': 'fas fa-paint-brush',
                'is_active': True
            }
        ]
    
    def create_object(self, data):
        """Create category object matching the Category model"""
        category, created = self.get_or_create_safe(
            Category,
            defaults={
                'name_ar': data['name_ar'],
                'description': data['description'],
                'description_ar': data['description_ar'],
                'icon': data['icon'],
                'is_active': data['is_active']
            },
            name=data['name']
        )
        
        if category:
            action = "Created" if created else "Updated"
            self.log_success(f"{action} category: {data['name']}")
            return True
        
        return False

if __name__ == '__main__':
    seeder = CategoriesSeeder()
    seeder.seed()

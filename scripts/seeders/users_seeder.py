#!/usr/bin/env python
"""
Users Seeder for SkillSwap
Seeds users with comprehensive data matching the User model
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
from accounts.models import User, UserSkill

class UsersSeeder(BaseSeeder):
    """Seeder for users matching the User model exactly"""
    
    def get_dependencies(self):
        """Users don't depend on other models for basic creation"""
        return []
    
    def get_data(self):
        """Return users data matching User model fields exactly"""
        return [
            {
                'email': 'ahmed.developer@skillswap.com',
                'first_name': 'أحمد',
                'last_name': 'محمد حسن',
                'bio': 'مطور ويب متخصص في React و Django مع خبرة 5+ سنوات في تطوير التطبيقات الحديثة. أحب مشاركة المعرفة وتعليم الآخرين أحدث تقنيات البرمجة.',
                'phone': '+201234567890',
                'location': 'القاهرة، مصر',
                'points_balance': 750,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Django Web Development',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    },
                    {
                        'name': 'React.js Development',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Python Programming',
                        'level': 'expert',
                        'years_of_experience': 6,
                        'is_verified': True
                    },
                    {
                        'name': 'Database Design',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': False
                    }
                ]
            },
            {
                'email': 'sara.designer@skillswap.com',
                'first_name': 'سارة',
                'last_name': 'أحمد علي',
                'bio': 'مصممة جرافيك إبداعية متخصصة في تصميم الهويات البصرية والمواد التسويقية. أستخدم أحدث أدوات التصميم لإنتاج أعمال فنية مميزة.',
                'phone': '+201234567891',
                'location': 'الإسكندرية، مصر',
                'points_balance': 520,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Logo Design',
                        'level': 'expert',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Adobe Photoshop',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    },
                    {
                        'name': 'Brand Identity Design',
                        'level': 'advanced',
                        'years_of_experience': 3,
                        'is_verified': True
                    },
                    {
                        'name': 'UI/UX Design',
                        'level': 'intermediate',
                        'years_of_experience': 2,
                        'is_verified': False
                    }
                ]
            },
            {
                'email': 'omar.marketer@skillswap.com',
                'first_name': 'عمر',
                'last_name': 'خالد محمود',
                'bio': 'خبير تسويق رقمي مع تخصص في إعلانات فيسبوك وجوجل. ساعدت أكثر من 100 شركة في تحسين حضورها الرقمي وزيادة مبيعاتها.',
                'phone': '+201234567892',
                'location': 'الجيزة، مصر',
                'points_balance': 680,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Facebook Ads Management',
                        'level': 'expert',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Google Ads',
                        'level': 'advanced',
                        'years_of_experience': 3,
                        'is_verified': True
                    },
                    {
                        'name': 'SEO Optimization',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Social Media Strategy',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    }
                ]
            },
            {
                'email': 'fatima.writer@skillswap.com',
                'first_name': 'فاطمة',
                'last_name': 'علي حسين',
                'bio': 'كاتبة محتوى ومترجمة محترفة بين العربية والإنجليزية. أتخصص في كتابة المحتوى التسويقي والتقني والأدبي بأسلوب جذاب ومؤثر.',
                'phone': '+201234567893',
                'location': 'المنصورة، مصر',
                'points_balance': 420,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Content Writing',
                        'level': 'expert',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Arabic-English Translation',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    },
                    {
                        'name': 'Copywriting',
                        'level': 'advanced',
                        'years_of_experience': 3,
                        'is_verified': True
                    },
                    {
                        'name': 'Technical Writing',
                        'level': 'intermediate',
                        'years_of_experience': 2,
                        'is_verified': False
                    }
                ]
            },
            {
                'email': 'hassan.photographer@skillswap.com',
                'first_name': 'حسن',
                'last_name': 'محمود أحمد',
                'bio': 'مصور فوتوغرافي ومحرر فيديو محترف مع شغف خاص بالتصوير الطبيعي والبورتريه. أقدم خدمات التصوير للأحداث والمناسبات الخاصة.',
                'phone': '+201234567894',
                'location': 'أسوان، مصر',
                'points_balance': 380,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Portrait Photography',
                        'level': 'expert',
                        'years_of_experience': 6,
                        'is_verified': True
                    },
                    {
                        'name': 'Event Photography',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Video Editing',
                        'level': 'advanced',
                        'years_of_experience': 3,
                        'is_verified': False
                    },
                    {
                        'name': 'Photo Retouching',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    }
                ]
            },
            {
                'email': 'nour.teacher@skillswap.com',
                'first_name': 'نور',
                'last_name': 'حسام الدين',
                'bio': 'معلمة لغة إنجليزية ومدربة تطوير شخصي معتمدة. أساعد الطلاب على تحسين مهاراتهم اللغوية وتطوير قدراتهم الشخصية والمهنية.',
                'phone': '+201234567895',
                'location': 'طنطا، مصر',
                'points_balance': 290,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'English Teaching',
                        'level': 'expert',
                        'years_of_experience': 7,
                        'is_verified': True
                    },
                    {
                        'name': 'Personal Development Coaching',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Presentation Skills',
                        'level': 'advanced',
                        'years_of_experience': 5,
                        'is_verified': True
                    },
                    {
                        'name': 'IELTS Preparation',
                        'level': 'expert',
                        'years_of_experience': 6,
                        'is_verified': True
                    }
                ]
            },
            {
                'email': 'khaled.consultant@skillswap.com',
                'first_name': 'خالد',
                'last_name': 'إبراهيم سالم',
                'bio': 'مستشار أعمال ومدير مشاريع معتمد مع خبرة 8+ سنوات في مساعدة الشركات الناشئة والمتوسطة على تحسين عملياتها وزيادة أرباحها.',
                'phone': '+201234567896',
                'location': 'الرياض، السعودية',
                'points_balance': 850,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Business Consulting',
                        'level': 'expert',
                        'years_of_experience': 8,
                        'is_verified': True
                    },
                    {
                        'name': 'Project Management',
                        'level': 'expert',
                        'years_of_experience': 7,
                        'is_verified': True
                    },
                    {
                        'name': 'Financial Planning',
                        'level': 'advanced',
                        'years_of_experience': 6,
                        'is_verified': True
                    },
                    {
                        'name': 'Market Research',
                        'level': 'advanced',
                        'years_of_experience': 5,
                        'is_verified': False
                    }
                ]
            },
            {
                'email': 'layla.fitness@skillswap.com',
                'first_name': 'ليلى',
                'last_name': 'حسن محمد',
                'bio': 'مدربة لياقة بدنية معتمدة ومتخصصة في اليوغا والتأمل. أساعد الأشخاص على تحقيق أهدافهم الصحية وتحسين نمط حياتهم.',
                'phone': '+201234567897',
                'location': 'عمان، الأردن',
                'points_balance': 340,
                'password': 'skillswap123',
                'is_active': True,
                'skills': [
                    {
                        'name': 'Personal Training',
                        'level': 'expert',
                        'years_of_experience': 5,
                        'is_verified': True
                    },
                    {
                        'name': 'Yoga Instruction',
                        'level': 'expert',
                        'years_of_experience': 6,
                        'is_verified': True
                    },
                    {
                        'name': 'Nutrition Counseling',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': True
                    },
                    {
                        'name': 'Meditation Coaching',
                        'level': 'advanced',
                        'years_of_experience': 4,
                        'is_verified': False
                    }
                ]
            }
        ]
    
    def create_object(self, data):
        """Create user object with skills matching the User and UserSkill models"""
        # Extract skills data
        skills_data = data.pop('skills', [])
        password = data.pop('password')
        
        # Create user
        user, created = self.get_or_create_safe(
            User,
            defaults={
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'bio': data['bio'],
                'phone': data['phone'],
                'location': data['location'],
                'points_balance': data['points_balance'],
                'is_active': data['is_active']
            },
            email=data['email']
        )
        
        if not user:
            return False
        
        if created:
            user.set_password(password)
            user.save()
            self.log_success(f"Created user: {data['email']}")
        else:
            self.log_info(f"Updated user: {data['email']}")
        
        # Create user skills using correct field names
        for skill_data in skills_data:
            skill, skill_created = self.get_or_create_safe(
                UserSkill,
                defaults={
                    'level': skill_data['level'],
                    'years_of_experience': skill_data['years_of_experience'],
                    'is_verified': skill_data['is_verified']
                },
                user=user,
                name=skill_data['name']  # Use 'name' instead of 'skill_name'
            )
            
            if skill and skill_created:
                self.log_success(f"  Added skill: {skill_data['name']} ({skill_data['level']})")
        
        return True

if __name__ == '__main__':
    seeder = UsersSeeder()
    seeder.seed()

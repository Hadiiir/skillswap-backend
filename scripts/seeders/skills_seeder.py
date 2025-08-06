#!/usr/bin/env python
"""
Skills Seeder for SkillSwap
Seeds skills with comprehensive data matching all Skill model fields
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
from skills.models import Category, Skill, SkillImage, SkillFAQ
from accounts.models import User
import random

class SkillsSeeder(BaseSeeder):
    """Seeder for skills matching all Skill model fields exactly"""
    
    def get_dependencies(self):
        """Skills depend on Categories and Users"""
        return ['skills.Category', 'accounts.User']
    
    def get_data(self):
        """Return skills data matching all Skill model fields"""
        return [
            {
                'title': 'تطوير تطبيقات الويب بـ React',
                'title_ar': 'تطوير تطبيقات الويب بـ React',
                'description': 'تعلم كيفية بناء تطبيقات ويب تفاعلية وحديثة باستخدام React.js مع أفضل الممارسات والأدوات الحديثة',
                'description_ar': 'تعلم كيفية بناء تطبيقات ويب تفاعلية وحديثة باستخدام React.js مع أفضل الممارسات والأدوات الحديثة',
                'category_name': 'البرمجة وتطوير الويب',
                'user_email': 'ahmed.developer@skillswap.com',
                'points_required': 150,
                'estimated_duration': '40 ساعة',
                'language': 'both',
                'difficulty': 'intermediate',
                'status': 'active',
                'is_featured': True,
                'total_orders': 100,
                'average_rating': 4.5,
                'total_reviews': 80,
                'tags': 'react,javascript,frontend,web development',
                'meta_description': 'تعلم كيفية بناء تطبيقات الويب التفاعلية باستخدام React.js',
                'faqs': [
                    {
                        'question': 'هل أحتاج خبرة سابقة في React؟',
                        'question_ar': 'هل أحتاج خبرة سابقة في React؟',
                        'answer': 'لا، سنبدأ من الأساسيات ولكن يُفضل معرفة JavaScript',
                        'answer_ar': 'لا، سنبدأ من الأساسيات ولكن يُفضل معرفة JavaScript',
                        'order': 1
                    },
                    {
                        'question': 'كم من الوقت أحتاج لإتقان React؟',
                        'question_ar': 'كم من الوقت أحتاج لإتقان React؟',
                        'answer': 'مع الممارسة المنتظمة، يمكن إتقان الأساسيات في 4-6 أسابيع',
                        'answer_ar': 'مع الممارسة المنتظمة، يمكن إتقان الأساسيات في 4-6 أسابيع',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'تصميم الهويات البصرية الاحترافية',
                'title_ar': 'تصميم الهويات البصرية الاحترافية',
                'description': 'تعلم كيفية تصميم هويات بصرية متكاملة للشركات والعلامات التجارية باستخدام أدوات التصميم الحديثة',
                'description_ar': 'تعلم كيفية تصميم هويات بصرية متكاملة للشركات والعلامات التجارية باستخدام أدوات التصميم الحديثة',
                'category_name': 'التصميم الجرافيكي',
                'user_email': 'sara.designer@skillswap.com',
                'points_required': 120,
                'estimated_duration': '30 ساعة',
                'language': 'both',
                'difficulty': 'intermediate',
                'status': 'active',
                'is_featured': True,
                'total_orders': 85,
                'average_rating': 4.7,
                'total_reviews': 65,
                'tags': 'logo design,branding,adobe illustrator,visual identity',
                'meta_description': 'تعلم تصميم الهويات البصرية الاحترافية باستخدام أدوات التصميم الحديثة',
                'faqs': [
                    {
                        'question': 'ما هي الأدوات المطلوبة؟',
                        'question_ar': 'ما هي الأدوات المطلوبة؟',
                        'answer': 'Adobe Illustrator أو Figma، وسنوفر البدائل المجانية',
                        'answer_ar': 'Adobe Illustrator أو Figma، وسنوفر البدائل المجانية',
                        'order': 1
                    },
                    {
                        'question': 'هل سأحصل على شهادة؟',
                        'question_ar': 'هل سأحصل على شهادة؟',
                        'answer': 'نعم، ستحصل على شهادة إتمام معتمدة من المنصة',
                        'answer_ar': 'نعم، ستحصل على شهادة إتمام معتمدة من المنصة',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'استراتيجيات التسويق الرقمي المتقدمة',
                'title_ar': 'استراتيجيات التسويق الرقمي المتقدمة',
                'description': 'تعلم أحدث استراتيجيات التسويق الرقمي وكيفية بناء حملات تسويقية ناجحة عبر منصات مختلفة',
                'description_ar': 'تعلم أحدث استراتيجيات التسويق الرقمي وكيفية بناء حملات تسويقية ناجحة عبر منصات مختلفة',
                'category_name': 'التسويق الرقمي',
                'user_email': 'omar.marketer@skillswap.com',
                'points_required': 180,
                'estimated_duration': '35 ساعة',
                'language': 'both',
                'difficulty': 'advanced',
                'status': 'active',
                'is_featured': True,
                'total_orders': 120,
                'average_rating': 4.6,
                'total_reviews': 95,
                'tags': 'digital marketing,seo,social media,google ads,analytics',
                'meta_description': 'تعلم أحدث استراتيجيات التسويق الرقمي وكيفية بناء حملات تسويقية ناجحة عبر منصات مختلفة',
                'faqs': [
                    {
                        'question': 'هل سأتعلم إعلانات فيسبوك وجوجل؟',
                        'question_ar': 'هل سأتعلم إعلانات فيسبوك وجوجل؟',
                        'answer': 'نعم، سنغطي جميع المنصات الإعلانية الرئيسية',
                        'answer_ar': 'نعم، سنغطي جميع المنصات الإعلانية الرئيسية',
                        'order': 1
                    },
                    {
                        'question': 'هل أحتاج ميزانية للتطبيق العملي؟',
                        'question_ar': 'هل أحتاج ميزانية للتطبيق العملي؟',
                        'answer': 'سنوفر حسابات تجريبية، لكن ميزانية صغيرة ستكون مفيدة',
                        'answer_ar': 'سنوفر حسابات تجريبية، لكن ميزانية صغيرة ستكون مفيدة',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'كتابة المحتوى الإبداعي والتسويقي',
                'title_ar': 'كتابة المحتوى الإبداعي والتسويقي',
                'description': 'تطوير مهارات الكتابة الإبداعية وكتابة المحتوى التسويقي الذي يجذب الجمهور ويحقق النتائج',
                'description_ar': 'تطوير مهارات الكتابة الإبداعية وكتابة المحتوى التسويقي الذي يجذب الجمهور ويحقق النتائج',
                'category_name': 'الكتابة والترجمة',
                'user_email': 'fatima.writer@skillswap.com',
                'points_required': 100,
                'estimated_duration': '25 ساعة',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 70,
                'average_rating': 4.4,
                'total_reviews': 50,
                'tags': 'content writing,copywriting,seo writing,creative writing',
                'meta_description': 'تطوير مهارات الكتابة الإبداعية وكتابة المحتوى التسويقي الذي يجذب الجمهور ويحقق النتائج',
                'faqs': [
                    {
                        'question': 'هل أحتاج خبرة سابقة في الكتابة؟',
                        'question_ar': 'هل أحتاج خبرة سابقة في الكتابة؟',
                        'answer': 'لا، سنبدأ من الأساسيات وننمي المهارات تدريجياً',
                        'answer_ar': 'لا، سنبدأ من الأساسيات وننمي المهارات تدريجياً',
                        'order': 1
                    },
                    {
                        'question': 'ما أنواع المحتوى التي سأتعلم كتابتها؟',
                        'question_ar': 'ما أنواع المحتوى التي سأتعلم كتابتها؟',
                        'answer': 'مقالات، منشورات اجتماعية، رسائل بريدية، ومحتوى إعلاني',
                        'answer_ar': 'مقالات، منشورات اجتماعية، رسائل بريدية، ومحتوى إعلاني',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'التصوير الفوتوغرافي الاحترافي',
                'title_ar': 'التصوير الفوتوغرافي الاحترافي',
                'description': 'تعلم أساسيات وتقنيات التصوير الفوتوغرافي الاحترافي مع التركيز على التصوير الطبيعي والبورتريه',
                'description_ar': 'تعلم أساسيات وتقنيات التصوير الفوتوغرافي الاحترافي مع التركيز على التصوير الطبيعي والبورتريه',
                'category_name': 'التصوير والفيديو',
                'user_email': 'hassan.photographer@skillswap.com',
                'points_required': 80,
                'estimated_duration': '20 ساعة',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 50,
                'average_rating': 4.5,
                'total_reviews': 35,
                'tags': 'photography,portrait,nature,lighting,composition',
                'meta_description': 'تعلم أساسيات وتقنيات التصوير الفوتوغرافي الاحترافي مع التركيز على التصوير الطبيعي والبورتريه',
                'faqs': [
                    {
                        'question': 'هل يمكنني استخدام كاميرا الهاتف؟',
                        'question_ar': 'هل يمكنني استخدام كاميرا الهاتف؟',
                        'answer': 'يُفضل كاميرا احترافية، لكن يمكن البدء بكاميرا هاتف متقدمة',
                        'answer_ar': 'يُفضل كاميرا احترافية، لكن يمكن البدء بكاميرا هاتف متقدمة',
                        'order': 1
                    },
                    {
                        'question': 'هل سنتعلم تحرير الصور؟',
                        'question_ar': 'هل سنتعلم تحرير الصور؟',
                        'answer': 'نعم، سنغطي أساسيات التحرير باستخدام Lightroom',
                        'answer_ar': 'نعم، سنغطي أساسيات التحرير باستخدام Lightroom',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'تطوير تطبيقات الويب بـ Django المتقدمة',
                'title_ar': 'تطوير تطبيقات الويب بـ Django المتقدمة',
                'description': 'دورة شاملة لتعلم تطوير تطبيقات الويب الحديثة باستخدام Django مع أفضل الممارسات والتقنيات المتقدمة. ستتعلم بناء APIs قوية، إدارة قواعد البيانات، الأمان، والنشر على الخوادم السحابية.',
                'description_ar': 'دورة شاملة لتعلم تطوير تطبيقات الويب الحديثة باستخدام Django مع أفضل الممارسات والتقنيات المتقدمة. ستتعلم بناء APIs قوية، إدارة قواعد البيانات، الأمان، والنشر على الخوادم السحابية.',
                'category_name': 'البرمجة وتطوير الويب',
                'user_email': 'ahmed.developer@skillswap.com',
                'points_required': 200,
                'estimated_duration': '6-8 أسابيع',
                'language': 'both',
                'difficulty': 'advanced',
                'status': 'active',
                'is_featured': True,
                'total_orders': 45,
                'average_rating': 4.8,
                'total_reviews': 32,
                'tags': 'django,python,web development,rest api,backend,postgresql,redis,celery',
                'meta_description': 'تعلم Django المتقدم لتطوير تطبيقات ويب قوية وقابلة للتوسع مع أفضل الممارسات',
                'faqs': [
                    {
                        'question': 'ما هي المتطلبات المسبقة لهذه الدورة؟',
                        'question_ar': 'ما هي المتطلبات المسبقة لهذه الدورة؟',
                        'answer': 'يجب أن تكون لديك معرفة أساسية بـ Python و HTML/CSS وفهم مبادئ البرمجة الكائنية',
                        'answer_ar': 'يجب أن تكون لديك معرفة أساسية بـ Python و HTML/CSS وفهم مبادئ البرمجة الكائنية',
                        'order': 1
                    },
                    {
                        'question': 'هل ستحصل على شهادة إتمام؟',
                        'question_ar': 'هل ستحصل على شهادة إتمام؟',
                        'answer': 'نعم، ستحصل على شهادة معتمدة من المنصة بعد إتمام جميع المتطلبات والمشاريع',
                        'answer_ar': 'نعم، ستحصل على شهادة معتمدة من المنصة بعد إتمام جميع المتطلبات والمشاريع',
                        'order': 2
                    },
                    {
                        'question': 'كم من الوقت أحتاج يومياً للدراسة؟',
                        'question_ar': 'كم من الوقت أحتاج يومياً للدراسة؟',
                        'answer': 'ننصح بتخصيص 2-3 ساعات يومياً للحصول على أفضل النتائج',
                        'answer_ar': 'ننصح بتخصيص 2-3 ساعات يومياً للحصول على أفضل النتائج',
                        'order': 3
                    }
                ]
            },
            {
                'title': 'تصميم الهويات البصرية الاحترافية',
                'title_ar': 'تصميم الهويات البصرية الاحترافية',
                'description': 'تعلم كيفية تصميم هويات بصرية متكاملة ومؤثرة للشركات والعلامات التجارية. ستتقن استخدام أدوات التصميم المتقدمة وفهم علم نفس الألوان والخطوط لإنتاج تصاميم تترك أثراً قوياً.',
                'description_ar': 'تعلم كيفية تصميم هويات بصرية متكاملة ومؤثرة للشركات والعلامات التجارية. ستتقن استخدام أدوات التصميم المتقدمة وفهم علم نفس الألوان والخطوط لإنتاج تصاميم تترك أثراً قوياً.',
                'category_name': 'التصميم الجرافيكي والإبداعي',
                'user_email': 'sara.designer@skillswap.com',
                'points_required': 180,
                'estimated_duration': '4-6 أسابيع',
                'language': 'both',
                'difficulty': 'intermediate',
                'status': 'active',
                'is_featured': True,
                'total_orders': 38,
                'average_rating': 4.9,
                'total_reviews': 28,
                'tags': 'logo design,branding,adobe illustrator,photoshop,visual identity,color theory',
                'meta_description': 'دورة شاملة لتعلم تصميم الهويات البصرية الاحترافية والشعارات المميزة',
                'faqs': [
                    {
                        'question': 'ما هي البرامج المطلوبة؟',
                        'question_ar': 'ما هي البرامج المطلوبة؟',
                        'answer': 'ستحتاج إلى Adobe Illustrator و Photoshop، وسنوفر بدائل مجانية مثل Figma',
                        'answer_ar': 'ستحتاج إلى Adobe Illustrator و Photoshop، وسنوفر بدائل مجانية مثل Figma',
                        'order': 1
                    },
                    {
                        'question': 'هل أحتاج خبرة سابقة في التصميم؟',
                        'question_ar': 'هل أحتاج خبرة سابقة في التصميم؟',
                        'answer': 'لا، الدورة مصممة للمبتدئين والمتوسطين، وسنبدأ من الأساسيات',
                        'answer_ar': 'لا، الدورة مصممة للمبتدئين والمتوسطين، وسنبدأ من الأساسيات',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'استراتيجيات التسويق الرقمي المتقدمة',
                'title_ar': 'استراتيجيات التسويق الرقمي المتقدمة',
                'description': 'دورة متخصصة في أحدث استراتيجيات التسويق الرقمي وإدارة الحملات الإعلانية المدفوعة. ستتعلم كيفية بناء استراتيجية تسويقية شاملة، تحليل البيانات، وتحسين معدلات التحويل لتحقيق أفضل عائد على الاستثمار.',
                'description_ar': 'دورة متخصصة في أحدث استراتيجيات التسويق الرقمي وإدارة الحملات الإعلانية المدفوعة. ستتعلم كيفية بناء استراتيجية تسويقية شاملة، تحليل البيانات، وتحسين معدلات التحويل لتحقيق أفضل عائد على الاستثمار.',
                'category_name': 'التسويق الرقمي والإلكتروني',
                'user_email': 'omar.marketer@skillswap.com',
                'points_required': 220,
                'estimated_duration': '5-7 أسابيع',
                'language': 'both',
                'difficulty': 'advanced',
                'status': 'active',
                'is_featured': True,
                'total_orders': 52,
                'average_rating': 4.7,
                'total_reviews': 41,
                'tags': 'digital marketing,facebook ads,google ads,seo,social media,analytics,conversion optimization',
                'meta_description': 'تعلم استراتيجيات التسويق الرقمي المتقدمة وإدارة الحملات الإعلانية بكفاءة عالية',
                'faqs': [
                    {
                        'question': 'هل سأتعلم إعلانات فيسبوك وجوجل؟',
                        'question_ar': 'هل سأتعلم إعلانات فيسبوك وجوجل؟',
                        'answer': 'نعم، سنغطي جميع المنصات الإعلانية الرئيسية بالتفصيل مع أمثلة عملية',
                        'answer_ar': 'نعم، سنغطي جميع المنصات الإعلانية الرئيسية بالتفصيل مع أمثلة عملية',
                        'order': 1
                    },
                    {
                        'question': 'هل أحتاج ميزانية إعلانية للتطبيق؟',
                        'question_ar': 'هل أحتاج ميزانية إعلانية للتطبيق؟',
                        'answer': 'سنوفر حسابات تجريبية، لكن ميزانية صغيرة (50-100$) ستكون مفيدة للتطبيق الفعلي',
                        'answer_ar': 'سنوفر حسابات تجريبية، لكن ميزانية صغيرة (50-100$) ستكون مفيدة للتطبيق الفعلي',
                        'order': 2
                    }
                ]
            },
            {
                'title': 'كتابة المحتوى الإبداعي والتسويقي',
                'title_ar': 'كتابة المحتوى الإبداعي والتسويقي',
                'description': 'طور مهاراتك في كتابة المحتوى الجذاب والمؤثر للمواقع ووسائل التواصل الاجتماعي. ستتعلم تقنيات الكتابة الإقناعية، تحسين المحتوى لمحركات البحث، وكيفية إنشاء محتوى يحقق أهدافك التسويقية.',
                'description_ar': 'طور مهاراتك في كتابة المحتوى الجذاب والمؤثر للمواقع ووسائل التواصل الاجتماعي. ستتعلم تقنيات الكتابة الإقناعية، تحسين المحتوى لمحركات البحث، وكيفية إنشاء محتوى يحقق أهدافك التسويقية.',
                'category_name': 'الكتابة والترجمة والتحرير',
                'user_email': 'fatima.writer@skillswap.com',
                'points_required': 150,
                'estimated_duration': '4-5 أسابيع',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 29,
                'average_rating': 4.6,
                'total_reviews': 22,
                'tags': 'content writing,copywriting,seo writing,social media,blogging,storytelling',
                'meta_description': 'تعلم كتابة المحتوى الإبداعي والتسويقي الذي يجذب الجمهور ويحقق النتائج',
                'faqs': [
                    {
                        'question': 'هل أحتاج خبرة سابقة في الكتابة؟',
                        'question_ar': 'هل أحتاج خبرة سابقة في الكتابة؟',
                        'answer': 'لا، سنبدأ من الأساسيات وننمي المهارات تدريجياً مع التطبيق العملي',
                        'answer_ar': 'لا، سنبدأ من الأساسيات وننمي المهارات تدريجياً مع التطبيق العملي',
                        'order': 1
                    }
                ]
            },
            {
                'title': 'التصوير الفوتوغرافي الاحترافي',
                'title_ar': 'التصوير الفوتوغرافي الاحترافي',
                'description': 'تعلم أساسيات وتقنيات التصوير الفوتوغرافي الاحترافي من الصفر حتى الاحتراف. ستتقن استخدام الكاميرا، فهم الإضاءة، تقنيات التكوين، وأساسيات تحرير الصور لإنتاج صور مذهلة.',
                'description_ar': 'تعلم أساسيات وتقنيات التصوير الفوتوغرافي الاحترافي من الصفر حتى الاحتراف. ستتقن استخدام الكاميرا، فهم الإضاءة، تقنيات التكوين، وأساسيات تحرير الصور لإنتاج صور مذهلة.',
                'category_name': 'التصوير الفوتوغرافي المحترف',
                'user_email': 'hassan.photographer@skillswap.com',
                'points_required': 160,
                'estimated_duration': '3-4 أسابيع',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 24,
                'average_rating': 4.8,
                'total_reviews': 18,
                'tags': 'photography,portrait,lighting,composition,camera,editing,lightroom',
                'meta_description': 'دورة شاملة لتعلم التصوير الفوتوغرافي الاحترافي من البداية حتى الاحتراف',
                'faqs': [
                    {
                        'question': 'هل يمكنني استخدام كاميرا الهاتف؟',
                        'question_ar': 'هل يمكنني استخدام كاميرا الهاتف؟',
                        'answer': 'يُفضل كاميرا DSLR أو Mirrorless، لكن يمكن البدء بكاميرا هاتف متقدمة',
                        'answer_ar': 'يُفضل كاميرا DSLR أو Mirrorless، لكن يمكن البدء بكاميرا هاتف متقدمة',
                        'order': 1
                    }
                ]
            },
            {
                'title': 'تدريس اللغة الإنجليزية للمبتدئين',
                'title_ar': 'تدريس اللغة الإنجليزية للمبتدئين',
                'description': 'برنامج تعليمي شامل لتعلم اللغة الإنجليزية من الصفر مع التركيز على المحادثة والتطبيق العملي. ستتقن القواعد الأساسية، المفردات الضرورية، ومهارات التحدث والاستماع.',
                'description_ar': 'برنامج تعليمي شامل لتعلم اللغة الإنجليزية من الصفر مع التركيز على المحادثة والتطبيق العملي. ستتقن القواعد الأساسية، المفردات الضرورية، ومهارات التحدث والاستماع.',
                'category_name': 'التعليم والتدريب المهني',
                'user_email': 'nour.teacher@skillswap.com',
                'points_required': 120,
                'estimated_duration': '8-10 أسابيع',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 67,
                'average_rating': 4.9,
                'total_reviews': 54,
                'tags': 'english teaching,conversation,grammar,vocabulary,speaking,listening',
                'meta_description': 'تعلم اللغة الإنجليزية من الصفر مع معلمة خبيرة ومنهج تفاعلي مميز',
                'faqs': [
                    {
                        'question': 'كم مرة في الأسبوع ستكون الجلسات؟',
                        'question_ar': 'كم مرة في الأسبوع ستكون الجلسات؟',
                        'answer': 'جلستان أسبوعياً مدة كل جلسة ساعة ونصف مع واجبات منزلية',
                        'answer_ar': 'جلستان أسبوعياً مدة كل جلسة ساعة ونصف مع واجبات منزلية',
                        'order': 1
                    }
                ]
            },
            {
                'title': 'استشارات الأعمال وإدارة المشاريع',
                'title_ar': 'استشارات الأعمال وإدارة المشاريع',
                'description': 'احصل على استشارة متخصصة لتطوير عملك وإدارة مشاريعك بكفاءة عالية. ستتعلم أفضل الممارسات في إدارة المشاريع، التخطيط الاستراتيجي، وحل المشكلات التجارية المعقدة.',
                'description_ar': 'احصل على استشارة متخصصة لتطوير عملك وإدارة مشاريعك بكفاءة عالية. ستتعلم أفضل الممارسات في إدارة المشاريع، التخطيط الاستراتيجي، وحل المشكلات التجارية المعقدة.',
                'category_name': 'الأعمال والاستشارات المهنية',
                'user_email': 'khaled.consultant@skillswap.com',
                'points_required': 300,
                'estimated_duration': '6-8 أسابيع',
                'language': 'both',
                'difficulty': 'advanced',
                'status': 'active',
                'is_featured': True,
                'total_orders': 31,
                'average_rating': 4.9,
                'total_reviews': 25,
                'tags': 'business consulting,project management,strategy,planning,leadership',
                'meta_description': 'استشارات أعمال متخصصة وتدريب على إدارة المشاريع من خبير معتمد',
                'faqs': [
                    {
                        'question': 'هل الاستشارة مناسبة للشركات الناشئة؟',
                        'question_ar': 'هل الاستشارة مناسبة للشركات الناشئة؟',
                        'answer': 'نعم، لدي خبرة واسعة مع الشركات الناشئة والمتوسطة والكبيرة',
                        'answer_ar': 'نعم، لدي خبرة واسعة مع الشركات الناشئة والمتوسطة والكبيرة',
                        'order': 1
                    }
                ]
            },
            {
                'title': 'تدريب اللياقة البدنية واليوغا',
                'title_ar': 'تدريب اللياقة البدنية واليوغا',
                'description': 'برنامج تدريبي شامل للياقة البدنية واليوغا مصمم خصيصاً لاحتياجاتك الشخصية. ستحصل على خطة تدريب مخصصة، نصائح غذائية، وجلسات يوغا للاسترخاء والمرونة.',
                'description_ar': 'برنامج تدريبي شامل للياقة البدنية واليوغا مصمم خصيصاً لاحتياجاتك الشخصية. ستحصل على خطة تدريب مخصصة، نصائح غذائية، وجلسات يوغا للاسترخاء والمرونة.',
                'category_name': 'الصحة واللياقة البدنية',
                'user_email': 'layla.fitness@skillswap.com',
                'points_required': 140,
                'estimated_duration': '4-6 أسابيع',
                'language': 'both',
                'difficulty': 'beginner',
                'status': 'active',
                'is_featured': False,
                'total_orders': 43,
                'average_rating': 4.8,
                'total_reviews': 35,
                'tags': 'fitness,yoga,personal training,nutrition,wellness,meditation',
                'meta_description': 'تدريب شخصي للياقة البدنية واليوغا مع مدربة معتمدة وخبيرة',
                'faqs': [
                    {
                        'question': 'هل أحتاج معدات رياضية خاصة؟',
                        'question_ar': 'هل أحتاج معدات رياضية خاصة؟',
                        'answer': 'سنبدأ بتمارين وزن الجسم، وسأرشدك للمعدات المناسبة لاحقاً',
                        'answer_ar': 'سنبدأ بتمارين وزن الجسم، وسأرشدك للمعدات المناسبة لاحقاً',
                        'order': 1
                    }
                ]
            }
        ]
    
    def create_object(self, data):
        """Create skill object with all related data matching the Skill model exactly"""
        # Get category
        try:
            category = Category.objects.get(name=data['category_name'])
        except Category.DoesNotExist:
            self.log_error(f"Category not found: {data['category_name']}")
            return False
        
        # Get user
        try:
            user = User.objects.get(email=data['user_email'])
        except User.DoesNotExist:
            self.log_error(f"User not found: {data['user_email']}")
            return False
        
        # Extract FAQs data
        faqs_data = data.pop('faqs', [])
        
        # Create skill with all model fields
        skill, created = self.get_or_create_safe(
            Skill,
            defaults={
                'title_ar': data['title_ar'],
                'description': data['description'],
                'description_ar': data['description_ar'],
                'category': category,
                'user': user,
                'points_required': data['points_required'],
                'estimated_duration': data['estimated_duration'],
                'language': data['language'],
                'difficulty': data['difficulty'],
                'status': data['status'],
                'is_featured': data['is_featured'],
                'total_orders': data['total_orders'],
                'average_rating': data['average_rating'],
                'total_reviews': data['total_reviews'],
                'tags': data['tags'],
                'meta_description': data['meta_description']
            },
            title=data['title']
        )
        
        if not skill:
            return False
        
        action = "Created" if created else "Updated"
        self.log_success(f"{action} skill: {data['title']} by {user.get_full_name()}")
        
        # Create FAQs
        for faq_data in faqs_data:
            faq, faq_created = self.get_or_create_safe(
                SkillFAQ,
                defaults={
                    'question_ar': faq_data['question_ar'],
                    'answer': faq_data['answer'],
                    'answer_ar': faq_data['answer_ar'],
                    'order': faq_data['order']
                },
                skill=skill,
                question=faq_data['question']
            )
            
            if faq and faq_created:
                self.log_success(f"  Added FAQ: {faq_data['question'][:50]}...")
        
        return True

if __name__ == '__main__':
    seeder = SkillsSeeder()
    seeder.seed()

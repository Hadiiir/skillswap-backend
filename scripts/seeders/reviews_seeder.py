#!/usr/bin/env python
"""
Reviews Seeder for SkillSwap
Seeds reviews matching the Review model exactly
"""
import os
import sys
import django
from pathlib import Path
import random

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from reviews.models import Review
from points.models import Order

class ReviewsSeeder(BaseSeeder):
    """Seeder for reviews matching the Review model exactly"""
    
    def get_dependencies(self):
        """Reviews depend on completed Orders"""
        return ['points.Order']
    
    def get_data(self):
        """Generate reviews data for completed orders"""
        # Get completed orders that don't have reviews yet
        completed_orders = Order.objects.filter(
            status='completed'
        ).exclude(
            order_review__isnull=False
        )
        
        if not completed_orders.exists():
            self.log_warning("No completed orders found without reviews")
            return []
        
        reviews_data = []
        
        # Create reviews for 80% of completed orders (realistic percentage)
        orders_to_review = random.sample(
            list(completed_orders), 
            int(len(completed_orders) * 0.8)
        )
        
        for order in orders_to_review:
            # Generate realistic ratings (mostly positive)
            rating = self.generate_realistic_rating()
            
            review_data = {
                'reviewer': order.buyer,
                'reviewee': order.seller,
                'skill': order.skill,
                'order': order,
                'rating': rating,
                'comment': self.generate_review_comment(rating, order.skill),
                'communication_rating': self.generate_aspect_rating(rating),
                'quality_rating': self.generate_aspect_rating(rating),
                'delivery_rating': self.generate_aspect_rating(rating),
                'is_public': random.choice([True, True, True, False])  # 75% public
            }
            
            reviews_data.append(review_data)
        
        return reviews_data
    
    def generate_realistic_rating(self):
        """Generate realistic rating distribution (mostly 4-5 stars)"""
        weights = [0.02, 0.03, 0.15, 0.35, 0.45]  # 1-5 stars weights
        return random.choices(range(1, 6), weights=weights)[0]
    
    def generate_aspect_rating(self, overall_rating):
        """Generate aspect rating close to overall rating"""
        # Aspect ratings usually vary by ±1 from overall rating
        min_rating = max(1, overall_rating - 1)
        max_rating = min(5, overall_rating + 1)
        return random.randint(min_rating, max_rating)
    
    def generate_review_comment(self, rating, skill):
        """Generate realistic review comments based on rating"""
        if rating == 5:
            comments = [
                f"تجربة رائعة جداً! {skill.user.get_full_name()} محترف حقيقي في {skill.title}. تعلمت الكثير وأنصح الجميع بالتعامل معه.",
                f"أفضل مدرب تعاملت معه على الإطلاق. الشرح واضح والأمثلة عملية. شكراً لك على الصبر والاهتمام.",
                f"خدمة ممتازة وجودة عالية جداً. تم تسليم العمل في الوقت المحدد مع إضافات قيمة لم أتوقعها.",
                f"مدرب محترف ومتمكن. استفدت كثيراً من خبرته العملية. أنصح بشدة!",
                f"تجاوز توقعاتي بمراحل. التعامل راقي والنتائج مذهلة. سأتعامل معه مرة أخرى بالتأكيد."
            ]
        elif rating == 4:
            comments = [
                f"تجربة جيدة جداً مع {skill.user.get_full_name()}. تعلمت الكثير في {skill.title} وأنصح بالتعامل معه.",
                f"مدرب جيد ومتعاون. الشرح واضح والمادة مفيدة. كان بإمكان إضافة المزيد من الأمثلة العملية.",
                f"خدمة جيدة وجودة مقبولة. تم الالتزام بالمواعيد والمتطلبات.",
                f"راضي عن النتائج بشكل عام. هناك مجال للتحسين لكن التجربة إيجابية.",
                f"تعامل محترم ونتائج جيدة. أنصح بالتعامل معه."
            ]
        elif rating == 3:
            comments = [
                f"تجربة متوسطة. تعلمت بعض الأشياء المفيدة لكن كنت أتوقع أكثر.",
                f"الخدمة مقبولة لكن هناك مجال كبير للتحسين في طريقة الشرح.",
                f"نتائج متوسطة. التسليم كان في الوقت المحدد لكن الجودة أقل من المتوقع.",
                f"تعامل جيد لكن المحتوى كان أساسي أكثر من اللازم.",
                f"تجربة عادية. لا سيء ولا ممتاز."
            ]
        elif rating == 2:
            comments = [
                f"تجربة مخيبة للآمال. لم أحصل على القيمة المتوقعة مقابل النقاط المدفوعة.",
                f"الشرح غير واضح والأمثلة قليلة. كنت أتوقع مستوى أفضل.",
                f"تأخير في التسليم وجودة أقل من المطلوب. محتاج تحسين كبير.",
                f"لم أستفد كثيراً من الجلسات. المحتوى سطحي جداً.",
                f"خدمة ضعيفة ولا أنصح بها."
            ]
        else:  # rating == 1
            comments = [
                f"تجربة سيئة جداً. لم أتعلم شيئاً مفيداً وضيعت نقاطي.",
                f"غير محترف في التعامل والمحتوى ضعيف جداً. لا أنصح أبداً.",
                f"أسوأ تجربة على المنصة. تأخير شديد وجودة متدنية.",
                f"لم يلتزم بالمتطلبات المتفق عليها. تجربة محبطة.",
                f"خدمة سيئة جداً ولا تستحق النقاط المدفوعة."
            ]
        
        return self.get_random_choice(comments)
    
    def create_object(self, data):
        """Create review object matching the Review model exactly"""
        review, created = self.get_or_create_safe(
            Review,
            defaults={
                'reviewee': data['reviewee'],
                'skill': data['skill'],
                'rating': data['rating'],
                'comment': data['comment'],
                'communication_rating': data['communication_rating'],
                'quality_rating': data['quality_rating'],
                'delivery_rating': data['delivery_rating'],
                'is_public': data['is_public']
            },
            reviewer=data['reviewer'],
            order=data['order']
        )
        
        if review:
            action = "Created" if created else "Updated"
            self.log_success(f"{action} review: {data['rating']}⭐ for {data['skill'].title}")
            
            # Update skill ratings after creating review
            if created:
                data['skill'].update_rating()
            
            return True
        
        return False

if __name__ == '__main__':
    seeder = ReviewsSeeder()
    seeder.seed()

from django.db.models import Count, Sum, Avg, Q, F
from django.db.models.functions import TruncDate, TruncMonth
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.cache import cache
from accounts.models import User
from skills.models import Skill, Category, SkillExchange
from points.models import PointsTransaction
from payments.models import Payment
from reviews.models import Review
import json
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class AnalyticsService:
    """خدمة التحليلات المتقدمة للمنصة"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_platform_overview(self, days=30):
        """نظرة عامة على إحصائيات المنصة"""
        cache_key = f"platform_overview_{days}"
        overview = cache.get(cache_key)
        
        if overview is None:
            try:
                end_date = timezone.now()
                start_date = end_date - timedelta(days=days)
                

                total_users = User.objects.count()
                new_users = User.objects.filter(
                    date_joined__gte=start_date
                ).count()
                active_users = User.objects.filter(
                    last_login__gte=start_date
                ).count()
                

                total_skills = Skill.objects.filter(is_active=True).count()
                new_skills = Skill.objects.filter(
                    created_at__gte=start_date,
                    is_active=True
                ).count()
                

                from points.models import Order
                total_orders = Order.objects.count()
                new_orders = Order.objects.filter(
                    created_at__gte=start_date
                ).count()
                completed_orders = Order.objects.filter(
                    status='completed',
                    updated_at__gte=start_date
                ).count()
                

                total_revenue = Payment.objects.filter(
                    status='completed'
                ).aggregate(
                    total=Sum('amount')
                )['total'] or 0
                
                recent_revenue = Payment.objects.filter(
                    status='completed',
                    created_at__gte=start_date
                ).aggregate(
                    total=Sum('amount')
                )['total'] or 0
                

                previous_start = start_date - timedelta(days=days)
                previous_users = User.objects.filter(
                    date_joined__gte=previous_start,
                    date_joined__lt=start_date
                ).count()
                
                user_growth_rate = 0
                if previous_users > 0:
                    user_growth_rate = ((new_users - previous_users) / previous_users) * 100
                
                overview = {
                    'users': {
                        'total': total_users,
                        'new': new_users,
                        'active': active_users,
                        'growth_rate': round(user_growth_rate, 2)
                    },
                    'skills': {
                        'total': total_skills,
                        'new': new_skills
                    },
                    'orders': {
                        'total': total_orders,
                        'new': new_orders,
                        'completed': completed_orders,
                        'completion_rate': round(
                            (completed_orders / new_orders * 100) if new_orders > 0 else 0, 2
                        )
                    },
                    'revenue': {
                        'total': float(total_revenue),
                        'recent': float(recent_revenue)
                    },
                    'period': {
                        'days': days,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }
                

                cache.set(cache_key, overview, 3600)
                
            except Exception as e:
                self.logger.error(f"Error getting platform overview: {e}")
                overview = {}
        
        return overview
    
    def get_user_analytics(self, user_id, days=30):
        """تحليلات مفصلة لمستخدم معين"""
        cache_key = f"user_analytics_{user_id}_{days}"
        analytics = cache.get(cache_key)
        
        if analytics is None:
            try:
                user = User.objects.get(id=user_id)
                end_date = timezone.now()
                start_date = end_date - timedelta(days=days)
                

                from points.models import Order
                user_orders = Order.objects.filter(user=user)
                recent_orders = user_orders.filter(created_at__gte=start_date)
                

                points_earned = PointsTransaction.objects.filter(
                    user=user,
                    transaction_type='earn',
                    created_at__gte=start_date
                ).aggregate(total=Sum('amount'))['total'] or 0
                
                points_spent = PointsTransaction.objects.filter(
                    user=user,
                    transaction_type='spend',
                    created_at__gte=start_date
                ).aggregate(total=Sum('amount'))['total'] or 0
                

                favorite_categories = user_orders.values(
                    'skill__category__name_en'
                ).annotate(
                    count=Count('id')
                ).order_by('-count')[:5]
                

                avg_rating_given = Review.objects.filter(
                    reviewer=user,
                    created_at__gte=start_date
                ).aggregate(avg=Avg('rating'))['avg'] or 0
                
                avg_rating_received = Review.objects.filter(
                    skill__user=user,
                    created_at__gte=start_date
                ).aggregate(avg=Avg('rating'))['avg'] or 0
                
                analytics = {
                    'user_id': user_id,
                    'orders': {
                        'total': user_orders.count(),
                        'recent': recent_orders.count(),
                        'completed': recent_orders.filter(status='completed').count(),
                        'cancelled': recent_orders.filter(status='cancelled').count()
                    },
                    'points': {
                        'current_balance': user.points_balance,
                        'earned': int(points_earned),
                        'spent': int(points_spent),
                        'net': int(points_earned - points_spent)
                    },
                    'ratings': {
                        'given': round(float(avg_rating_given), 2),
                        'received': round(float(avg_rating_received), 2)
                    },
                    'favorite_categories': list(favorite_categories),
                    'activity_level': self._calculate_activity_level(user, days),
                    'period': {
                        'days': days,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }
                

                cache.set(cache_key, analytics, 1800)
                
            except Exception as e:
                self.logger.error(f"Error getting user analytics for {user_id}: {e}")
                analytics = {}
        
        return analytics
    
    def get_skills_analytics(self, days=30):
        """تحليلات المهارات والفئات"""
        cache_key = f"skills_analytics_{days}"
        analytics = cache.get(cache_key)
        
        if analytics is None:
            try:
                end_date = timezone.now()
                start_date = end_date - timedelta(days=days)
                

                from points.models import Order
                top_skills = Skill.objects.filter(
                    is_active=True
                ).annotate(
                    total_orders=Count('orders'),
                    recent_orders=Count(
                        'orders',
                        filter=Q(orders__created_at__gte=start_date)
                    ),
                    avg_rating=Avg('reviews__rating'),
                    total_revenue=Sum('orders__points_amount')
                ).order_by('-recent_orders')[:10]
                

                top_categories = Category.objects.annotate(
                    total_skills=Count('skills', filter=Q(skills__is_active=True)),
                    total_orders=Count('skills__orders'),
                    recent_orders=Count(
                        'skills__orders',
                        filter=Q(skills__orders__created_at__gte=start_date)
                    )
                ).order_by('-recent_orders')[:5]
                

                rating_distribution = Review.objects.filter(
                    created_at__gte=start_date
                ).values('rating').annotate(
                    count=Count('id')
                ).order_by('rating')
                

                promising_skills = Skill.objects.filter(
                    created_at__gte=start_date,
                    is_active=True
                ).annotate(
                    orders_count=Count('orders'),
                    avg_rating=Avg('reviews__rating')
                ).filter(
                    orders_count__gt=0
                ).order_by('-orders_count', '-avg_rating')[:5]
                
                analytics = {
                    'top_skills': [
                        {
                            'id': skill.id,
                            'title': skill.title,
                            'category': skill.category.name_en,
                            'total_orders': skill.total_orders,
                            'recent_orders': skill.recent_orders,
                            'avg_rating': round(float(skill.avg_rating or 0), 2),
                            'total_revenue': float(skill.total_revenue or 0)
                        }
                        for skill in top_skills
                    ],
                    'top_categories': [
                        {
                            'name': category.name_en,
                            'total_skills': category.total_skills,
                            'total_orders': category.total_orders,
                            'recent_orders': category.recent_orders
                        }
                        for category in top_categories
                    ],
                    'rating_distribution': list(rating_distribution),
                    'promising_skills': [
                        {
                            'id': skill.id,
                            'title': skill.title,
                            'orders_count': skill.orders_count,
                            'avg_rating': round(float(skill.avg_rating or 0), 2)
                        }
                        for skill in promising_skills
                    ],
                    'period': {
                        'days': days,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }
                

                cache.set(cache_key, analytics, 3600)
                
            except Exception as e:
                self.logger.error(f"Error getting skills analytics: {e}")
                analytics = {}
        
        return analytics
    
    def get_financial_analytics(self, days=30):
        """التحليلات المالية"""
        cache_key = f"financial_analytics_{days}"
        analytics = cache.get(cache_key)
        
        if analytics is None:
            try:
                end_date = timezone.now()
                start_date = end_date - timedelta(days=days)
                

                total_payments = Payment.objects.filter(
                    status='completed',
                    created_at__gte=start_date
                ).aggregate(
                    total_amount=Sum('amount'),
                    count=Count('id')
                )
                

                daily_revenue = Payment.objects.filter(
                    status='completed',
                    created_at__gte=start_date
                ).annotate(
                    date=TruncDate('created_at')
                ).values('date').annotate(
                    revenue=Sum('amount'),
                    transactions=Count('id')
                ).order_by('date')
                

                points_transactions = PointsTransaction.objects.filter(
                    created_at__gte=start_date
                ).values('transaction_type').annotate(
                    total_amount=Sum('amount'),
                    count=Count('id')
                )
                

                avg_transaction_value = total_payments['total_amount'] / total_payments['count'] if total_payments['count'] > 0 else 0
                

                payment_methods = Payment.objects.filter(
                    created_at__gte=start_date
                ).values('payment_method').annotate(
                    count=Count('id'),
                    total_amount=Sum('amount')
                ).order_by('-count')
                
                analytics = {
                    'summary': {
                        'total_revenue': float(total_payments['total_amount'] or 0),
                        'total_transactions': total_payments['count'],
                        'avg_transaction_value': round(float(avg_transaction_value), 2)
                    },
                    'daily_revenue': [
                        {
                            'date': item['date'].isoformat(),
                            'revenue': float(item['revenue']),
                            'transactions': item['transactions']
                        }
                        for item in daily_revenue
                    ],
                    'points_transactions': list(points_transactions),
                    'payment_methods': list(payment_methods),
                    'period': {
                        'days': days,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }
                

                cache.set(cache_key, analytics, 3600)
                
            except Exception as e:
                self.logger.error(f"Error getting financial analytics: {e}")
                analytics = {}
        
        return analytics
    
    def _calculate_activity_level(self, user, days):
        """حساب مستوى نشاط المستخدم"""
        try:
            end_date = timezone.now()
            start_date = end_date - timedelta(days=days)
            

            from points.models import Order
            active_days = Order.objects.filter(
                user=user,
                created_at__gte=start_date
            ).annotate(
                date=TruncDate('created_at')
            ).values('date').distinct().count()
            

            activity_ratio = active_days / days if days > 0 else 0
            

            if activity_ratio >= 0.7:
                return 'high'
            elif activity_ratio >= 0.3:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            self.logger.error(f"Error calculating activity level: {e}")
            return 'unknown'
    
    def get_growth_trends(self, months=6):
        """اتجاهات النمو الشهرية"""
        cache_key = f"growth_trends_{months}"
        trends = cache.get(cache_key)
        
        if trends is None:
            try:
                end_date = timezone.now()
                start_date = end_date - timedelta(days=months * 30)
                

                user_growth = User.objects.filter(
                    date_joined__gte=start_date
                ).annotate(
                    month=TruncMonth('date_joined')
                ).values('month').annotate(
                    new_users=Count('id')
                ).order_by('month')
                

                skill_growth = Skill.objects.filter(
                    created_at__gte=start_date
                ).annotate(
                    month=TruncMonth('created_at')
                ).values('month').annotate(
                    new_skills=Count('id')
                ).order_by('month')
                

                revenue_growth = Payment.objects.filter(
                    status='completed',
                    created_at__gte=start_date
                ).annotate(
                    month=TruncMonth('created_at')
                ).values('month').annotate(
                    revenue=Sum('amount'),
                    transactions=Count('id')
                ).order_by('month')
                
                trends = {
                    'user_growth': list(user_growth),
                    'skill_growth': list(skill_growth),
                    'revenue_growth': [
                        {
                            'month': item['month'],
                            'revenue': float(item['revenue']),
                            'transactions': item['transactions']
                        }
                        for item in revenue_growth
                    ],
                    'period': {
                        'months': months,
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    }
                }
                

                cache.set(cache_key, trends, 21600)
                
            except Exception as e:
                self.logger.error(f"Error getting growth trends: {e}")
                trends = {}
        
        return trends
    
    def get_platform_stats(self):
        """Get overall platform statistics"""
        try:
            stats = {
                'total_users': User.objects.count(),
                'active_users': User.objects.filter(
                    last_login__gte=timezone.now() - timedelta(days=30)
                ).count(),
                'total_skills': Skill.objects.count(),
                'total_exchanges': SkillExchange.objects.count(),
                'completed_exchanges': SkillExchange.objects.filter(
                    status='completed'
                ).count(),
            }
            
            # Calculate success rate
            if stats['total_exchanges'] > 0:
                stats['success_rate'] = (
                    stats['completed_exchanges'] / stats['total_exchanges']
                ) * 100
            else:
                stats['success_rate'] = 0
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error getting platform stats: {e}")
            return {}
    
    def get_skill_analytics(self, skill):
        """Get analytics for a specific skill"""
        try:
            analytics = {
                'total_exchanges': skill.exchanges_as_offered.count(),
                'completed_exchanges': skill.exchanges_as_offered.filter(
                    status='completed'
                ).count(),
                'pending_exchanges': skill.exchanges_as_offered.filter(
                    status='pending'
                ).count(),
            }
            
            # Calculate average rating for this skill
            avg_rating = skill.exchanges_as_offered.aggregate(
                avg_rating=Avg('reviews__rating')
            )['avg_rating']
            analytics['average_rating'] = avg_rating or 0
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error getting skill analytics: {e}")
            return {}
    
    def get_trending_data(self, days=30):
        """Get trending skills and categories"""
        try:
            since_date = timezone.now() - timedelta(days=days)
            
            # Trending skills
            trending_skills = Skill.objects.annotate(
                recent_exchanges=Count(
                    'exchanges_as_offered',
                    filter=Q(exchanges_as_offered__created_at__gte=since_date)
                )
            ).order_by('-recent_exchanges')[:10]
            
            # Trending categories
            trending_categories = Skill.objects.filter(
                exchanges_as_offered__created_at__gte=since_date
            ).values('category').annotate(
                exchange_count=Count('exchanges_as_offered')
            ).order_by('-exchange_count')[:10]
            
            return {
                'trending_skills': trending_skills,
                'trending_categories': trending_categories
            }
            
        except Exception as e:
            self.logger.error(f"Error getting trending data: {e}")
            return {'trending_skills': [], 'trending_categories': []}

# Global instance
analytics_service = AnalyticsService()

from django.db.models import Q, Count, Avg, Case, When, IntegerField
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from skills.models import Skill
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class AdvancedSearchEngine:
    """Advanced search functionality for SkillSwap"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def search_skills(self, query, filters=None, sort_by='relevance', limit=20):
        """Advanced skill search with filters and sorting"""
        try:
            skills = Skill.objects.all()
            
            # Apply text search
            if query:
                skills = skills.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(category__icontains=query)
                )
            
            # Apply filters
            if filters:
                if 'category' in filters:
                    skills = skills.filter(category=filters['category'])
                
                if 'min_rating' in filters:
                    skills = skills.annotate(
                        avg_rating=Avg('exchanges_as_offered__reviews__rating')
                    ).filter(avg_rating__gte=filters['min_rating'])
                
                if 'location' in filters:
                    skills = skills.filter(user__location__icontains=filters['location'])
            
            # Apply sorting
            if sort_by == 'popularity':
                skills = skills.annotate(
                    exchange_count=Count('exchanges_as_offered')
                ).order_by('-exchange_count')
            elif sort_by == 'rating':
                skills = skills.annotate(
                    avg_rating=Avg('exchanges_as_offered__reviews__rating')
                ).order_by('-avg_rating')
            elif sort_by == 'recent':
                skills = skills.order_by('-created_at')
            else:  # relevance
                skills = skills.order_by('-created_at')
            
            return skills[:limit]
            
        except Exception as e:
            self.logger.error(f"Error in skill search: {e}")
            return Skill.objects.none()
    
    def search_users(self, query, filters=None, limit=20):
        """Advanced user search"""
        try:
            users = User.objects.filter(is_active=True)
            
            # Apply text search
            if query:
                users = users.filter(
                    Q(username__icontains=query) |
                    Q(first_name__icontains=query) |
                    Q(last_name__icontains=query) |
                    Q(bio__icontains=query)
                )
            
            # Apply filters
            if filters:
                if 'location' in filters:
                    users = users.filter(location__icontains=filters['location'])
                
                if 'min_rating' in filters:
                    users = users.annotate(
                        avg_rating=Avg('received_reviews__rating')
                    ).filter(avg_rating__gte=filters['min_rating'])
            
            # Order by relevance (users with more skills and better ratings)
            users = users.annotate(
                skill_count=Count('skills_offered'),
                avg_rating=Avg('received_reviews__rating')
            ).order_by('-skill_count', '-avg_rating')
            
            return users[:limit]
            
        except Exception as e:
            self.logger.error(f"Error in user search: {e}")
            return User.objects.none()
    
    def get_search_suggestions(self, query, limit=5):
        """Get search suggestions based on partial query"""
        try:
            suggestions = []
            
            # Skill suggestions
            skill_suggestions = Skill.objects.filter(
                title__icontains=query
            ).values_list('title', flat=True)[:limit]
            
            suggestions.extend([{'type': 'skill', 'text': title} for title in skill_suggestions])
            
            # Category suggestions
            category_suggestions = Skill.objects.filter(
                category__icontains=query
            ).values_list('category', flat=True).distinct()[:limit]
            
            suggestions.extend([{'type': 'category', 'text': cat} for cat in category_suggestions])
            
            return suggestions[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting search suggestions: {e}")
            return []

# Global instance
search_engine = AdvancedSearchEngine()

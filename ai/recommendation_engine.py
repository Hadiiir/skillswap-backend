import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from django.core.cache import cache
from django.db.models import Count, Avg, Q
from skills.models import Skill, Category, SkillExchange
from accounts.models import User
from reviews.models import Review
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

class AIRecommendationEngine:
    """محرك التوصيات الذكي باستخدام الذكاء الاصطناعي"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.svd = TruncatedSVD(n_components=50)
        self.logger = logging.getLogger(__name__)
        
    def get_user_recommendations(self, user_id, limit=10):
        """الحصول على توصيات شخصية للمستخدم"""
        cache_key = f"user_recommendations_{user_id}_{limit}"
        recommendations = cache.get(cache_key)
        
        if recommendations is None:
            try:

                user = User.objects.get(id=user_id)
                

                content_based = self._get_content_based_recommendations(user, limit)
                collaborative = self._get_collaborative_recommendations(user, limit)
                trending = self._get_trending_recommendations(limit)
                

                recommendations = self._merge_recommendations(
                    content_based, collaborative, trending, limit
                )
                

                cache.set(cache_key, recommendations, 3600)
                
            except Exception as e:
                self.logger.error(f"Error getting recommendations for user {user_id}: {e}")
                recommendations = []
                
        return recommendations
    
    def _get_content_based_recommendations(self, user, limit):
        """توصيات بناءً على المحتوى"""
        try:

            user_skills = user.skills_offered.all()[:5]
            
            if not user_skills:
                return []
            

            user_text = " ".join([
                skill.title + " " + skill.description 
                for skill in user_skills
            ])
            

            all_skills = Skill.objects.filter(is_active=True).exclude(
                id__in=[skill.id for skill in user_skills]
            )
            
            if not all_skills:
                return []
            

            skill_texts = [user_text] + [
                skill.title + " " + skill.description 
                for skill in all_skills
            ]
            

            tfidf_matrix = self.vectorizer.fit_transform(skill_texts)
            

            similarity_scores = cosine_similarity(
                tfidf_matrix[0:1], tfidf_matrix[1:]
            ).flatten()
            

            skill_indices = similarity_scores.argsort()[::-1][:limit]
            
            recommendations = []
            for idx in skill_indices:
                if similarity_scores[idx] > 0.1: 
                    skill = all_skills[idx]
                    recommendations.append({
                        'skill': skill,
                        'score': float(similarity_scores[idx]),
                        'reason': 'content_based'
                    })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error in content-based recommendations: {e}")
            return []
    
    def _get_collaborative_recommendations(self, user, limit):
        """توصيات تعاونية بناءً على المستخدمين المشابهين"""
        try:

            similar_users = self._find_similar_users(user, 10)
            
            if not similar_users:
                return []
            

            similar_user_skills = Skill.objects.filter(
                exchanges_as_offered__requester__in=similar_users,
                is_active=True
            ).exclude(
                exchanges_as_offered__requester=user
            ).annotate(
                popularity=Count('exchanges_as_offered'),
                avg_rating=Avg('exchanges_as_offered__reviews__rating')
            ).order_by('-popularity', '-avg_rating')[:limit]
            
            recommendations = []
            for skill in similar_user_skills:
                recommendations.append({
                    'skill': skill,
                    'score': min(skill.popularity / 10.0, 1.0), 
                    'reason': 'collaborative'
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error in collaborative recommendations: {e}")
            return []
    
    def _get_trending_recommendations(self, limit):
        """المهارات الرائجة حالياً"""
        try:
            last_month = timezone.now() - timedelta(days=30)
            
            trending_skills = Skill.objects.filter(
                is_active=True,
                created_at__gte=last_month
            ).annotate(
                recent_orders=Count(
                    'exchanges_as_offered',
                    filter=Q(exchanges_as_offered__created_at__gte=last_month)
                ),
                avg_rating=Avg('exchanges_as_offered__reviews__rating')
            ).filter(
                recent_orders__gt=0
            ).order_by('-recent_orders', '-avg_rating')[:limit]
            
            recommendations = []
            for skill in trending_skills:
                recommendations.append({
                    'skill': skill,
                    'score': min(skill.recent_orders / 5.0, 1.0),  
                    'reason': 'trending'
                })
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error in trending recommendations: {e}")
            return []
    
    def _find_similar_users(self, user, limit):
        """البحث عن مستخدمين مشابهين"""
        try:

            user_skills = set(user.skills_offered.values_list('id', flat=True))
            
            if not user_skills:
                return []
            
            similar_users = User.objects.filter(
                exchanges_as_offered__skill_offered__id__in=user_skills
            ).exclude(
                id=user.id
            ).annotate(
                common_skills=Count('exchanges_as_offered__skill_offered', distinct=True)
            ).filter(
                common_skills__gte=2  
            ).order_by('-common_skills')[:limit]
            
            return similar_users
            
        except Exception as e:
            self.logger.error(f"Error finding similar users: {e}")
            return []
    
    def _merge_recommendations(self, content_based, collaborative, trending, limit):
        """دمج التوصيات من مصادر مختلفة"""
        try:

            weights = {
                'content_based': 0.4,
                'collaborative': 0.4,
                'trending': 0.2
            }
            

            all_recommendations = {}
            

            for rec in content_based:
                skill_id = rec['skill'].id
                if skill_id not in all_recommendations:
                    all_recommendations[skill_id] = {
                        'skill': rec['skill'],
                        'total_score': 0,
                        'reasons': []
                    }
                all_recommendations[skill_id]['total_score'] += (
                    rec['score'] * weights['content_based']
                )
                all_recommendations[skill_id]['reasons'].append('content_based')
            

            for rec in collaborative:
                skill_id = rec['skill'].id
                if skill_id not in all_recommendations:
                    all_recommendations[skill_id] = {
                        'skill': rec['skill'],
                        'total_score': 0,
                        'reasons': []
                    }
                all_recommendations[skill_id]['total_score'] += (
                    rec['score'] * weights['collaborative']
                )
                all_recommendations[skill_id]['reasons'].append('collaborative')
            

            for rec in trending:
                skill_id = rec['skill'].id
                if skill_id not in all_recommendations:
                    all_recommendations[skill_id] = {
                        'skill': rec['skill'],
                        'total_score': 0,
                        'reasons': []
                    }
                all_recommendations[skill_id]['total_score'] += (
                    rec['score'] * weights['trending']
                )
                all_recommendations[skill_id]['reasons'].append('trending')
            

            final_recommendations = sorted(
                all_recommendations.values(),
                key=lambda x: x['total_score'],
                reverse=True
            )[:limit]
            
            return final_recommendations
            
        except Exception as e:
            self.logger.error(f"Error merging recommendations: {e}")
            return []
    
    def get_similar_skills(self, skill_id, limit=5):
        """الحصول على مهارات مشابهة لمهارة معينة"""
        cache_key = f"similar_skills_{skill_id}_{limit}"
        similar_skills = cache.get(cache_key)
        
        if similar_skills is None:
            try:
                skill = Skill.objects.get(id=skill_id, is_active=True)
                

                category_skills = Skill.objects.filter(
                    category=skill.category,
                    is_active=True
                ).exclude(id=skill_id)
                

                tag_skills = Skill.objects.filter(
                    tags__overlap=skill.tags,
                    is_active=True
                ).exclude(id=skill_id)
                

                all_skills = (category_skills | tag_skills).distinct()
                
                if all_skills.exists():

                    skill_text = skill.title + " " + skill.description
                    skill_texts = [skill_text] + [
                        s.title + " " + s.description for s in all_skills
                    ]
                    
                    tfidf_matrix = self.vectorizer.fit_transform(skill_texts)
                    similarity_scores = cosine_similarity(
                        tfidf_matrix[0:1], tfidf_matrix[1:]
                    ).flatten()
                    

                    skill_indices = similarity_scores.argsort()[::-1][:limit]
                    
                    similar_skills = []
                    for idx in skill_indices:
                        if similarity_scores[idx] > 0.1:
                            similar_skill = list(all_skills)[idx]
                            similar_skills.append({
                                'skill': similar_skill,
                                'similarity': float(similarity_scores[idx])
                            })
                else:
                    similar_skills = []
                

                cache.set(cache_key, similar_skills, 3600)
                
            except Exception as e:
                self.logger.error(f"Error getting similar skills for {skill_id}: {e}")
                similar_skills = []
        
        return similar_skills
    
    def update_user_preferences(self, user_id, skill_id, action):
        """تحديث تفضيلات المستخدم بناءً على الأفعال"""
        try:

            cache_keys = [
                f"user_recommendations_{user_id}_*",
                f"similar_skills_{skill_id}_*"
            ]
            
            for key_pattern in cache_keys:
                cache.delete_pattern(key_pattern)
            

            self.logger.info(f"Updated preferences for user {user_id}, skill {skill_id}, action {action}")
            
        except Exception as e:
            self.logger.error(f"Error updating user preferences: {e}")

# Global instance
recommendation_engine = AIRecommendationEngine()

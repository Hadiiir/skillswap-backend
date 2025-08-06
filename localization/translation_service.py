import requests
from django.conf import settings
from django.core.cache import cache
from django.utils.translation import get_language
import json

class TranslationService:
    """خدمة الترجمة المتقدمة"""
    
    def __init__(self):
        self.supported_languages = ['ar', 'en', 'fr', 'es', 'de']
        self.google_translate_api_key = getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', None)
    
    def auto_translate_skill(self, skill):
        """ترجمة تلقائية للمهارة"""
        translations = {}
        
        # تحديد اللغة الأصلية
        source_lang = self._detect_language(skill.title + ' ' + skill.description)
        
        for target_lang in self.supported_languages:
            if target_lang == source_lang:
                continue
                
            # ترجمة العنوان
            translated_title = self._translate_text(
                skill.title, source_lang, target_lang
            )
            
            # ترجمة الوصف
            translated_description = self._translate_text(
                skill.description, source_lang, target_lang
            )
            
            translations[target_lang] = {
                'title': translated_title,
                'description': translated_description
            }
        
        return translations
    
    def _detect_language(self, text):
        """كشف لغة النص"""
        cache_key = f"lang_detect_{hash(text)}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        # استخدام Google Translate API لكشف اللغة
        if self.google_translate_api_key:
            try:
                url = f"https://translation.googleapis.com/language/translate/v2/detect"
                params = {
                    'key': self.google_translate_api_key,
                    'q': text[:500]  # أول 500 حرف فقط
                }
                
                response = requests.post(url, json=params)
                result = response.json()
                
                if 'data' in result and 'detections' in result['data']:
                    detected_lang = result['data']['detections'][0][0]['language']
                    cache.set(cache_key, detected_lang, 3600)
                    return detected_lang
                    
            except Exception as e:
                print(f"Language detection error: {e}")
        
        # كشف بسيط بناءً على الأحرف
        arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars > 0 and arabic_chars / total_chars > 0.3:
            return 'ar'
        else:
            return 'en'
    
    def _translate_text(self, text, source_lang, target_lang):
        """ترجمة النص"""
        if not text or source_lang == target_lang:
            return text
        
        cache_key = f"translation_{hash(text)}_{source_lang}_{target_lang}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            return cached_result
        
        # استخدام Google Translate API
        if self.google_translate_api_key:
            try:
                url = "https://translation.googleapis.com/language/translate/v2"
                params = {
                    'key': self.google_translate_api_key,
                    'q': text,
                    'source': source_lang,
                    'target': target_lang,
                    'format': 'text'
                }
                
                response = requests.post(url, json=params)
                result = response.json()
                
                if 'data' in result and 'translations' in result['data']:
                    translated_text = result['data']['translations'][0]['translatedText']
                    cache.set(cache_key, translated_text, 86400)  # يوم واحد
                    return translated_text
                    
            except Exception as e:
                print(f"Translation error: {e}")
        
        # إرجاع النص الأصلي في حالة فشل الترجمة
        return text
    
    def get_localized_content(self, obj, field_name, language=None):
        """الحصول على المحتوى المترجم"""
        if not language:
            language = get_language() or 'en'
        
        # البحث عن الحقل المترجم
        localized_field = f"{field_name}_{language}"
        
        if hasattr(obj, localized_field):
            localized_value = getattr(obj, localized_field)
            if localized_value:
                return localized_value
        
        # إرجاع القيمة الافتراضية
        return getattr(obj, field_name, '')
    
    def create_multilingual_search_index(self):
        """إنشاء فهرس بحث متعدد اللغات"""
        from skills.models import Skill
        
        skills = Skill.objects.filter(status='active')
        search_index = {}
        
        for skill in skills:
            # إنشاء فهرس لكل لغة
            for lang in self.supported_languages:
                if lang not in search_index:
                    search_index[lang] = []
                
                title = self.get_localized_content(skill, 'title', lang)
                description = self.get_localized_content(skill, 'description', lang)
                
                search_index[lang].append({
                    'id': skill.id,
                    'title': title,
                    'description': description,
                    'category': self.get_localized_content(skill.category, 'name', lang),
                    'tags': skill.tags,
                    'searchable_text': f"{title} {description} {skill.tags}".lower()
                })
        
        # حفظ الفهرس في الكاش
        cache.set('multilingual_search_index', search_index, 3600)
        return search_index

# خدمة الترجمة
translation_service = TranslationService()

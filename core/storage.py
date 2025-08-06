import os
import uuid
from PIL import Image
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

class FileUploadService:
    """خدمة رفع الملفات المتقدمة"""
    
    ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ALLOWED_DOCUMENT_EXTENSIONS = ['.pdf', '.doc', '.docx', '.txt', '.zip', '.rar']
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def upload_image(file, folder='images', resize=None):
        """رفع وتحسين الصور"""
        try:
            # التحقق من نوع الملف
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext not in FileUploadService.ALLOWED_IMAGE_EXTENSIONS:
                return {'success': False, 'error': 'نوع الملف غير مدعوم'}
            
            # التحقق من حجم الملف
            if file.size > FileUploadService.MAX_IMAGE_SIZE:
                return {'success': False, 'error': 'حجم الملف كبير جداً'}
            
            # إنشاء اسم فريد للملف
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = f"{folder}/{unique_filename}"
            
            # فتح وتحسين الصورة
            image = Image.open(file)
            
            # تحويل RGBA إلى RGB إذا لزم الأمر
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            
            # تغيير حجم الصورة إذا طُلب ذلك
            if resize:
                image.thumbnail(resize, Image.Resampling.LANCZOS)
            
            # حفظ الصورة المحسنة
            from io import BytesIO
            output = BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # رفع الملف
            saved_path = default_storage.save(file_path, ContentFile(output.read()))
            file_url = default_storage.url(saved_path)
            
            return {
                'success': True,
                'file_path': saved_path,
                'file_url': file_url,
                'file_size': output.tell()
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def upload_document(file, folder='documents'):
        """رفع المستندات"""
        try:
            # التحقق من نوع الملف
            file_ext = os.path.splitext(file.name)[1].lower()
            if file_ext not in FileUploadService.ALLOWED_DOCUMENT_EXTENSIONS:
                return {'success': False, 'error': 'نوع الملف غير مدعوم'}
            
            # التحقق من حجم الملف
            if file.size > FileUploadService.MAX_DOCUMENT_SIZE:
                return {'success': False, 'error': 'حجم الملف كبير جداً'}
            
            # إنشاء اسم فريد للملف
            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = f"{folder}/{unique_filename}"
            
            # رفع الملف
            saved_path = default_storage.save(file_path, file)
            file_url = default_storage.url(saved_path)
            
            return {
                'success': True,
                'file_path': saved_path,
                'file_url': file_url,
                'file_size': file.size,
                'original_name': file.name
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def delete_file(file_path):
        """حذف ملف"""
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                return {'success': True}
            return {'success': False, 'error': 'الملف غير موجود'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

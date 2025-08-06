#!/usr/bin/env python3
"""
إصلاح الأخطاء النحوية في المشروع
"""

import os
import re
import sys

def fix_positional_arguments():
    """إصلاح مشاكل ترتيب المعاملات"""
    
    files_to_fix = [
        'ai/recommendation_engine.py',
        'search/advanced_search.py', 
        'analytics/services.py',
        'localization/translation_service.py',
        'security/advanced_security.py'
    ]
    
    fixes_applied = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"🔧 إصلاح {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # إصلاح مشاكل Case/When
            content = re.sub(
                r'Case$$\s*When\(([^,]+),\s*then=([^)]+)$$,\s*default=([^,]+),\s*output_field=([^)]+)\)',
                r'Case(When(\1, then=\2), default=\3, output_field=\4)',
                content
            )
            
            # إصلاح مشاكل annotate مع filter
            content = re.sub(
                r'Count$$([^,]+),\s*filter=([^)]+)$$',
                r'Count(\1, filter=\2)',
                content
            )
            
            content = re.sub(
                r'Sum$$([^,]+),\s*filter=([^)]+)$$',
                r'Sum(\1, filter=\2)',
                content
            )
            
            # إصلاح مشاكل sorted
            content = re.sub(
                r'sorted$$\s*([^,]+),\s*key=([^,]+),\s*reverse=([^)]+)$$',
                r'sorted(\1, key=\2, reverse=\3)',
                content
            )
            
            # إصلاح مشاكل requests.post
            content = re.sub(
                r'requests\.post$$\s*([^,]+),\s*json=([^)]+)$$',
                r'requests.post(\1, json=\2)',
                content
            )
            
            content = re.sub(
                r'requests\.post$$\s*([^,]+),\s*data=([^)]+)$$',
                r'requests.post(\1, data=\2)',
                content
            )
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixes_applied += 1
                print(f"✅ تم إصلاح {file_path}")
            else:
                print(f"ℹ️  لا توجد أخطاء في {file_path}")
        else:
            print(f"⚠️  الملف غير موجود: {file_path}")
    
    print(f"\n🎉 تم إصلاح {fixes_applied} ملف")
    return fixes_applied

def validate_python_syntax():
    """التحقق من صحة بناء الجملة Python"""
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    errors_found = 0
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # محاولة تجميع الكود
            compile(content, file_path, 'exec')
            
        except SyntaxError as e:
            print(f"❌ خطأ نحوي في {file_path}:")
            print(f"   السطر {e.lineno}: {e.msg}")
            if e.text:
                print(f"   الكود: {e.text.strip()}")
            errors_found += 1
            
        except Exception as e:
            print(f"⚠️  خطأ في قراءة {file_path}: {e}")
    
    if errors_found == 0:
        print("✅ جميع ملفات Python صحيحة نحوياً!")
    else:
        print(f"❌ تم العثور على {errors_found} خطأ نحوي")
    
    return errors_found

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إصلاح الأخطاء النحوية...")
    print("=" * 50)
    
    # إصلاح مشاكل ترتيب المعاملات
    fixes_applied = fix_positional_arguments()
    
    print("\n" + "=" * 50)
    print("🔍 التحقق من صحة بناء الجملة...")
    
    # التحقق من صحة بناء الجملة
    errors_found = validate_python_syntax()
    
    print("\n" + "=" * 50)
    
    if errors_found == 0:
        print("🎉 تم إصلاح جميع الأخطاء بنجاح!")
        return 0
    else:
        print("❌ لا تزال هناك أخطاء تحتاج إصلاح")
        return 1

if __name__ == "__main__":
    sys.exit(main())

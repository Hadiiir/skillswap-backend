#!/usr/bin/env python
"""
Base Seeder Class for SkillSwap
Provides common functionality for all seeders with comprehensive error handling
"""
import os
import sys
import django
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import random

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

class BaseSeeder(ABC):
    """Base class for all seeders with comprehensive functionality"""
    
    def __init__(self):
        self.created_count = 0
        self.updated_count = 0
        self.skipped_count = 0
        self.errors = []
        self.warnings = []
        self.seeder_name = self.__class__.__name__.replace('Seeder', '')
        self.start_time = None
        self.end_time = None
    
    def log_success(self, message: str):
        """Log success message with green color"""
        print(f"✅ {message}")
    
    def log_info(self, message: str):
        """Log info message with blue color"""
        print(f"ℹ️  {message}")
    
    def log_warning(self, message: str):
        """Log warning message with yellow color"""
        print(f"⚠️  {message}")
        self.warnings.append(message)
    
    def log_error(self, message: str, exception: Exception = None):
        """Log error message with red color"""
        error_msg = f"❌ {message}"
        if exception:
            error_msg += f" - {str(exception)}"
        print(error_msg)
        self.errors.append(error_msg)
    
    def get_or_create_safe(self, model_class, defaults: Dict[str, Any] = None, **lookup_fields) -> Tuple[Any, bool]:
        """
        Safely get or create an object with comprehensive error handling
        Returns (object, created) tuple or (None, False) on error
        """
        try:
            if defaults is None:
                defaults = {}
            
            obj, created = model_class.objects.get_or_create(
                defaults=defaults,
                **lookup_fields
            )
            
            if created:
                self.created_count += 1
                return obj, True
            else:
                # Update existing object with new defaults if provided
                updated = False
                for key, value in defaults.items():
                    if hasattr(obj, key) and getattr(obj, key) != value:
                        setattr(obj, key, value)
                        updated = True
                
                if updated:
                    obj.save()
                    self.updated_count += 1
                else:
                    self.skipped_count += 1
                
                return obj, False
                
        except Exception as e:
            self.log_error(f"Error creating/updating {model_class.__name__}", e)
            return None, False
    
    def bulk_create_safe(self, model_class, objects_list: List[Any]) -> List[Any]:
        """
        Safely bulk create objects with error handling
        Returns list of created objects
        """
        try:
            if not objects_list:
                return []
            
            created_objects = model_class.objects.bulk_create(
                objects_list, 
                ignore_conflicts=True,
                batch_size=100
            )
            
            self.created_count += len(created_objects)
            return created_objects
            
        except Exception as e:
            self.log_error(f"Error bulk creating {model_class.__name__} objects", e)
            return []
    
    def get_random_choice(self, choices_list: List[Any]) -> Any:
        """Get random choice from list safely"""
        if not choices_list:
            return None
        return random.choice(choices_list)
    
    def get_random_choices(self, choices_list: List[Any], count: int = None) -> List[Any]:
        """Get multiple random choices from list"""
        if not choices_list:
            return []
        
        if count is None:
            count = random.randint(1, min(3, len(choices_list)))
        
        count = min(count, len(choices_list))
        return random.sample(choices_list, count)
    
    def generate_random_rating(self, min_rating: float = 3.5, max_rating: float = 5.0) -> float:
        """Generate random rating within range"""
        return round(random.uniform(min_rating, max_rating), 2)
    
    def generate_random_points(self, min_points: int = 50, max_points: int = 500) -> int:
        """Generate random points within range"""
        return random.randint(min_points, max_points)
    
    def start_seeding(self):
        """Start the seeding process with timing"""
        self.start_time = datetime.now()
        self.log_info(f"Starting {self.seeder_name} seeding at {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def finish_seeding(self):
        """Finish the seeding process and show summary"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        
        print(f"\n{'='*50}")
        print(f"📊 {self.seeder_name} Seeder Summary")
        print(f"{'='*50}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"✅ Created: {self.created_count}")
        print(f"🔄 Updated: {self.updated_count}")
        print(f"⏭️  Skipped: {self.skipped_count}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors:
                print(f"   • {error}")
        else:
            print(f"\n🎉 {self.seeder_name} seeding completed successfully!")
        
        print(f"{'='*50}\n")
    
    def validate_dependencies(self, required_models: List[str]) -> bool:
        """
        Validate that required model data exists before seeding
        Returns True if all dependencies are met
        """
        from django.apps import apps
        
        missing_dependencies = []
        
        for model_name in required_models:
            try:
                app_label, model_name = model_name.split('.')
                model_class = apps.get_model(app_label, model_name)
                
                if not model_class.objects.exists():
                    missing_dependencies.append(f"{app_label}.{model_name}")
                    
            except (ValueError, LookupError) as e:
                self.log_error(f"Invalid model reference: {model_name}", e)
                return False
        
        if missing_dependencies:
            self.log_error(f"Missing required data for: {', '.join(missing_dependencies)}")
            self.log_info("Please run the required seeders first.")
            return False
        
        return True
    
    @abstractmethod
    def get_data(self) -> List[Dict[str, Any]]:
        """Return the data to be seeded - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def create_object(self, data: Dict[str, Any]) -> bool:
        """Create object from data - must be implemented by subclasses"""
        pass
    
    def get_dependencies(self) -> List[str]:
        """
        Return list of required model dependencies
        Override in subclasses if needed
        """
        return []
    
    def seed(self):
        """Main seeding method with comprehensive error handling"""
        self.start_seeding()
        
        try:
            # Check dependencies
            dependencies = self.get_dependencies()
            if dependencies and not self.validate_dependencies(dependencies):
                self.log_error("Dependency validation failed. Aborting seeding.")
                return
            
            # Get data to seed
            data_list = self.get_data()
            total_items = len(data_list)
            
            if total_items == 0:
                self.log_warning("No data to seed")
                return
            
            self.log_info(f"Processing {total_items} {self.seeder_name.lower()} items...")
            
            # Process each item
            for i, data in enumerate(data_list, 1):
                try:
                    success = self.create_object(data)
                    
                    # Progress indicator
                    if i % 10 == 0 or i == total_items:
                        progress = (i / total_items) * 100
                        self.log_info(f"Progress: {i}/{total_items} ({progress:.1f}%)")
                        
                except Exception as e:
                    self.log_error(f"Error processing item {i}: {data.get('name', 'Unknown')}", e)
                    continue
            
        except Exception as e:
            self.log_error(f"Fatal error in {self.seeder_name} seeding", e)
        
        finally:
            self.finish_seeding()

if __name__ == '__main__':
    print("This is the base seeder class. Run specific seeders instead.")
    print("Available seeders:")
    print("  - create_superuser_seeder.py")
    print("  - categories_seeder.py")
    print("  - users_seeder.py")
    print("  - points_seeder.py")
    print("  - skills_seeder.py")
    print("  - orders_seeder.py")
    print("  - reviews_seeder.py")
    print("  - notifications_seeder.py")
    print("  - payments_seeder.py")
    print("  - master_seeder.py (runs all)")

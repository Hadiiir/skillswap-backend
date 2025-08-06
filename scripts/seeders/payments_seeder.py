#!/usr/bin/env python
"""
Payments Seeder for SkillSwap
Seeds payment records matching the Payment model exactly
"""
import os
import sys
import django
from pathlib import Path
import random
from datetime import timedelta
import uuid
from decimal import Decimal

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillswap.settings')

# Setup Django
django.setup()

from base_seeder import BaseSeeder
from payments.models import Payment
from points.models import PointsPackage, PointsTransaction
from accounts.models import User
from django.utils import timezone

class PaymentsSeeder(BaseSeeder):
    """Seeder for payments matching the Payment model exactly"""
    
    def get_dependencies(self):
        """Payments depend on PointsPackages and Users"""
        return ['points.PointsPackage', 'accounts.User']
    
    def get_data(self):
        """Generate payments data"""
        payments_data = []
        
        # Get users and packages
        users = list(User.objects.filter(is_active=True, is_superuser=False))
        packages = list(PointsPackage.objects.filter(is_active=True))
        
        if not users or not packages:
            self.log_error("No users or packages found for payments")
            return []
        
        # Generate 30 sample payments
        for i in range(30):
            user = self.get_random_choice(users)
            package = self.get_random_choice(packages)
            
            # Calculate amount (with discount if applicable)
            discount_decimal = Decimal(str(package.discount_percentage)) / Decimal('100')
            amount = package.price * (Decimal('1') - discount_decimal)
            
            # Random payment method with realistic distribution
            payment_methods = [
                ('stripe', 0.4),
                ('paypal', 0.25),
                ('paymob', 0.15),
                ('vodafone_cash', 0.1),
                ('etisalat_cash', 0.05),
                ('orange_cash', 0.05)
            ]
            
            payment_method = self.weighted_random_choice(payment_methods)
            
            # Random status with realistic distribution
            status_choices = [
                ('completed', 0.8),  # 80% completed
                ('processing', 0.1),  # 10% processing
                ('failed', 0.05),    # 5% failed
                ('cancelled', 0.03), # 3% cancelled
                ('refunded', 0.02)   # 2% refunded
            ]
            
            status = self.weighted_random_choice(status_choices)
            
            # Generate timestamps
            created_at = timezone.now() - timedelta(days=random.randint(1, 90))
            
            payment_data = {
                'user': user,
                'points_package': package,
                'amount': amount,
                'currency': package.currency,
                'payment_method': payment_method,
                'status': status,
                'external_payment_id': self.generate_external_id(payment_method),
                'external_reference': f"REF_{random.randint(100000, 999999)}",
                'metadata': self.generate_metadata(payment_method, package),
                'failure_reason': self.generate_failure_reason(status),
                'created_at': created_at,
                'updated_at': created_at + timedelta(minutes=random.randint(1, 60)),
                'completed_at': created_at + timedelta(minutes=random.randint(5, 120)) if status == 'completed' else None
            }
            
            payments_data.append(payment_data)
        
        return payments_data
    
    def weighted_random_choice(self, choices):
        """Choose randomly based on weights"""
        total = sum(weight for choice, weight in choices)
        r = random.uniform(0, total)
        upto = 0
        for choice, weight in choices:
            if upto + weight >= r:
                return choice
            upto += weight
        return choices[-1][0]
    
    def generate_external_id(self, payment_method):
        """Generate realistic external payment ID based on method"""
        if payment_method == 'stripe':
            return f"pi_{uuid.uuid4().hex[:24]}"
        elif payment_method == 'paypal':
            return f"PAY-{uuid.uuid4().hex[:20].upper()}"
        elif payment_method == 'paymob':
            return f"PMB_{random.randint(1000000, 9999999)}"
        elif payment_method in ['vodafone_cash', 'etisalat_cash', 'orange_cash']:
            return f"TXN_{random.randint(100000000, 999999999)}"
        else:
            return f"PAY_{uuid.uuid4().hex[:16]}"
    
    def generate_metadata(self, payment_method, package):
        """Generate realistic metadata based on payment method"""
        base_metadata = {
            'package_name': package.name,
            'points': package.points,
            'discount_applied': package.discount_percentage > 0
        }
        
        if payment_method == 'stripe':
            base_metadata.update({
                'stripe_customer_id': f"cus_{uuid.uuid4().hex[:14]}",
                'payment_intent_id': f"pi_{uuid.uuid4().hex[:24]}",
                'card_last4': str(random.randint(1000, 9999)),
                'card_brand': random.choice(['visa', 'mastercard', 'amex'])
            })
        elif payment_method == 'paypal':
            base_metadata.update({
                'paypal_payer_id': f"PAYER{random.randint(100000, 999999)}",
                'paypal_email': f"user{random.randint(1000, 9999)}@example.com"
            })
        elif payment_method == 'paymob':
            base_metadata.update({
                'paymob_order_id': random.randint(1000000, 9999999),
                'integration_id': random.randint(100000, 999999)
            })
        elif payment_method in ['vodafone_cash', 'etisalat_cash', 'orange_cash']:
            base_metadata.update({
                'mobile_number': f"+2010{random.randint(10000000, 99999999)}",
                'operator': payment_method.replace('_cash', '').title()
            })
        
        return base_metadata
    
    def generate_failure_reason(self, status):
        """Generate failure reason for failed payments"""
        if status == 'failed':
            reasons = [
                "رصيد غير كافي في البطاقة",
                "تم رفض الدفع من البنك",
                "انتهت صلاحية البطاقة",
                "خطأ في بيانات البطاقة",
                "تم تجاوز الحد الأقصى للمعاملات"
            ]
            return self.get_random_choice(reasons)
        elif status == 'cancelled':
            return "تم إلغاء العملية من قبل المستخدم"
        elif status == 'refunded':
            return "تم استرداد المبلغ بناءً على طلب المستخدم"
        
        return ""
    
    def seed(self):
        """Seed payments"""
        self.log_info("Starting Payments seeding...")
        
        payments_data = self.get_data()
        
        for payment_data in payments_data:
            if self.create_object(payment_data):
                self.created_count += 1
        
        self.log_success("Payments seeding completed!")
        self.print_summary()
    
    def create_object(self, data):
        """Create payment object matching the Payment model exactly"""
        payment, created = self.get_or_create_safe(
            Payment,
            defaults={
                'points_package': data['points_package'],
                'amount': data['amount'],
                'currency': data['currency'],
                'payment_method': data['payment_method'],
                'status': data['status'],
                'external_payment_id': data['external_payment_id'],
                'external_reference': data['external_reference'],
                'metadata': data['metadata'],
                'failure_reason': data['failure_reason'],
                'created_at': data['created_at'],
                'updated_at': data['updated_at'],
                'completed_at': data['completed_at']
            },
            user=data['user'],
            external_payment_id=data['external_payment_id']
        )
        
        if payment:
            action = "Created" if created else "Updated"
            self.log_success(f"{action} payment: {data['payment_method']} - {data['status']} - ${data['amount']}")
            
            # Create corresponding points transaction for completed payments
            if created and data['status'] == 'completed':
                self.create_points_transaction(payment)
            
            return True
        
        return False
    
    def create_points_transaction(self, payment):
        """Create points transaction for completed payment"""
        try:
            # Get user's current balance
            current_balance = payment.user.points_balance
            
            transaction, created = PointsTransaction.objects.get_or_create(
                user=payment.user,
                payment_id=str(payment.id),
                defaults={
                    'transaction_type': 'purchase',
                    'amount': payment.points_package.points,
                    'status': 'completed',
                    'description': f"شراء حزمة {payment.points_package.name}",
                    'reference_id': payment.external_reference,
                    'balance_before': current_balance,
                    'balance_after': current_balance + payment.points_package.points,
                    'created_at': payment.completed_at,
                    'updated_at': payment.completed_at
                }
            )
            
            if created:
                # Update user's points balance
                payment.user.points_balance += payment.points_package.points
                payment.user.save(update_fields=['points_balance'])
                
                self.log_success(f"  Created points transaction: +{payment.points_package.points} points")
        
        except Exception as e:
            self.log_error(f"Error creating points transaction for payment {payment.id}", e)

if __name__ == '__main__':
    seeder = PaymentsSeeder()
    seeder.seed()

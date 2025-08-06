import stripe
import requests
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import Payment
from points.models import PointsTransaction

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentService:
    """خدمة الدفع الموحدة"""
    
    @staticmethod
    def create_stripe_payment(user, points_package, payment_method_id):
        """إنشاء دفعة Stripe"""
        try:
            # create Payment Intent
            intent = stripe.PaymentIntent.create(
                amount=int(points_package.discounted_price * 100),  
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                metadata={
                    'user_id': user.id,
                    'package_id': points_package.id,
                    'points': points_package.points
                }
            )
            
            payment = Payment.objects.create(
                user=user,
                points_package=points_package,
                amount=points_package.discounted_price,
                currency='USD',
                payment_method='stripe',
                external_payment_id=intent.id,
                status='processing'
            )
            
            if intent.status == 'succeeded':
                return PaymentService.complete_payment(payment)
            elif intent.status == 'requires_action':
                return {
                    'success': False,
                    'requires_action': True,
                    'client_secret': intent.client_secret,
                    'payment_id': payment.id
                }
            else:
                payment.status = 'failed'
                payment.failure_reason = f"Payment failed: {intent.status}"
                payment.save()
                return {'success': False, 'error': 'Payment failed'}
                
        except stripe.error.StripeError as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def create_paymob_payment(user, points_package, phone_number):
        """إنشاء دفعة Paymob"""
        try:

            auth_response = requests.post(
                'https://accept.paymob.com/api/auth/tokens',
                json={'api_key': settings.PAYMOB_API_KEY}
            )
            auth_token = auth_response.json()['token']
            
            order_response = requests.post(
                'https://accept.paymob.com/api/ecommerce/orders',
                json={
                    'auth_token': auth_token,
                    'delivery_needed': False,
                    'amount_cents': int(points_package.discounted_price * 100),
                    'currency': 'EGP',
                    'items': [{
                        'name': points_package.name,
                        'amount_cents': int(points_package.discounted_price * 100),
                        'description': f'{points_package.points} points package',
                        'quantity': 1
                    }]
                }
            )
            order_id = order_response.json()['id']
            
            payment_key_response = requests.post(
                'https://accept.paymob.com/api/acceptance/payment_keys',
                json={
                    'auth_token': auth_token,
                    'amount_cents': int(points_package.discounted_price * 100),
                    'expiration': 3600,
                    'order_id': order_id,
                    'billing_data': {
                        'apartment': 'NA',
                        'email': user.email,
                        'floor': 'NA',
                        'first_name': user.first_name,
                        'street': 'NA',
                        'building': 'NA',
                        'phone_number': phone_number,
                        'shipping_method': 'NA',
                        'postal_code': 'NA',
                        'city': 'NA',
                        'country': 'EG',
                        'last_name': user.last_name,
                        'state': 'NA'
                    },
                    'currency': 'EGP',
                    'integration_id': settings.PAYMOB_INTEGRATION_ID
                }
            )
            payment_key = payment_key_response.json()['token']
            
            payment = Payment.objects.create(
                user=user,
                points_package=points_package,
                amount=points_package.discounted_price,
                currency='EGP',
                payment_method='paymob',
                external_payment_id=str(order_id),
                external_reference=payment_key,
                status='pending'
            )
            
            return {
                'success': True,
                'payment_key': payment_key,
                'payment_id': payment.id,
                'iframe_url': f'https://accept.paymob.com/api/acceptance/iframes/{settings.PAYMOB_IFRAME_ID}?payment_token={payment_key}'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def complete_payment(payment):
        """إكمال الدفع وإضافة النقاط"""
        try:
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()
            
            user = payment.user
            points_to_add = payment.points_package.points
            
            transaction = PointsTransaction.objects.create(
                user=user,
                transaction_type='purchase',
                amount=points_to_add,
                status='completed',
                description=f'Purchased {payment.points_package.name}',
                payment_id=str(payment.id),
                balance_before=user.points_balance,
                balance_after=user.points_balance + points_to_add
            )
            
            user.points_balance += points_to_add
            user.total_earned_points += points_to_add
            user.save()
            
            return {
                'success': True,
                'payment': payment,
                'transaction': transaction,
                'new_balance': user.points_balance
            }
            
        except Exception as e:
            payment.status = 'failed'
            payment.failure_reason = str(e)
            payment.save()
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def handle_webhook(payment_method, data):
        """معالجة webhooks من بوابات الدفع"""
        if payment_method == 'stripe':
            return PaymentService.handle_stripe_webhook(data)
        elif payment_method == 'paymob':
            return PaymentService.handle_paymob_webhook(data)
    
    @staticmethod
    def handle_stripe_webhook(data):
        """معالجة Stripe webhook"""
        try:
            event = stripe.Event.construct_from(data, stripe.api_key)
            
            if event.type == 'payment_intent.succeeded':
                intent = event.data.object
                payment = Payment.objects.get(external_payment_id=intent.id)
                return PaymentService.complete_payment(payment)
                
            elif event.type == 'payment_intent.payment_failed':
                intent = event.data.object
                payment = Payment.objects.get(external_payment_id=intent.id)
                payment.status = 'failed'
                payment.failure_reason = intent.last_payment_error.message if intent.last_payment_error else 'Payment failed'
                payment.save()
                
            return {'success': True}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

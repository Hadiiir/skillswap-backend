from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
from .models import Payment
from .serializers import PaymentSerializer
import requests
import base64

class PaymentHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user's payment history",
        responses={200: PaymentSerializer(many=True)},
        tags=['Payments']
    )
    def get(self, request):
        payments = Payment.objects.filter(user=request.user).order_by('-created_at')
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)


class StripePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process Stripe payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'payment_method_id': openapi.Schema(type=openapi.TYPE_STRING, description='Stripe payment method ID')
            },
            required=['amount', 'currency', 'payment_method_id']
        ),
        responses={200: "Payment processed"},
        tags=['Payments']
    )
    def post(self, request):
        stripe_key = getattr(settings, 'STRIPE_SECRET_KEY', None)
        if not stripe_key:
            return Response({'error': 'Stripe not configured'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # TODO: إضافة منطق الدفع عبر Stripe هنا

        return Response({'message': 'Stripe payment endpoint - to be implemented'})


class PayPalPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process PayPal payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'paypal_order_id': openapi.Schema(type=openapi.TYPE_STRING, description='PayPal order ID')
            },
            required=['amount', 'currency', 'paypal_order_id']
        ),
        responses={200: "Payment processed"},
        tags=['Payments']
    )
    def post(self, request):
        paypal_client_id = getattr(settings, 'PAYPAL_CLIENT_ID', None)
        paypal_secret = getattr(settings, 'PAYPAL_SECRET', None)
        if not paypal_client_id or not paypal_secret:
            return Response({'error': 'PayPal not configured'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        amount = request.data.get("amount")
        currency = request.data.get("currency")
        paypal_order_id = request.data.get("paypal_order_id")

        if not all([amount, currency, paypal_order_id]):
            return Response({'error': 'Missing payment details'}, status=status.HTTP_400_BAD_REQUEST)

        # احصل على access token من PayPal
        auth = base64.b64encode(f"{paypal_client_id}:{paypal_secret}".encode()).decode()
        token_response = requests.post(
            "https://api-m.sandbox.paypal.com/v1/oauth2/token",
            headers={
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            data="grant_type=client_credentials"
        )
        if token_response.status_code != 200:
            return Response({'error': 'Failed to authenticate with PayPal'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = token_response.json().get('access_token')

        # تحقق من حالة الطلب
        order_response = requests.get(
            f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        if order_response.status_code != 200:
            return Response({'error': 'Failed to retrieve PayPal order'}, status=status.HTTP_400_BAD_REQUEST)

        order_data = order_response.json()
        if order_data.get("status") != "COMPLETED":
            return Response({'error': 'PayPal payment not completed'}, status=status.HTTP_400_BAD_REQUEST)

        # حفظ بيانات الدفع في قاعدة البيانات (مثال)
        Payment.objects.create(
            user=request.user,
            amount=amount,
            currency=currency,
            payment_method='paypal',
            status='completed',
            external_payment_id=paypal_order_id
        )

        return Response({'message': 'PayPal payment verified and processed'})


class PaymobPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process Paymob payment and return payment link",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount in EGP'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code', default='EGP')
            },
            required=['amount']
        ),
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'payment_url': openapi.Schema(type=openapi.TYPE_STRING, description='Redirect user to this payment link')
            }
        )},
        tags=['Payments']
    )
    def post(self, request):
        amount = request.data.get("amount")
        currency = request.data.get("currency", "EGP")

        required_keys = [
            'PAYMOB_API_KEY',
            'PAYMOB_INTEGRATION_ID',
            'PAYMOB_IFRAME_ID'
        ]
        missing = [key for key in required_keys if not getattr(settings, key, None)]

        if missing:
            return Response({'error': f'Missing Paymob config: {", ".join(missing)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        paymob_api_key = settings.PAYMOB_API_KEY
        integration_id = settings.PAYMOB_INTEGRATION_ID
        iframe_id = settings.PAYMOB_IFRAME_ID

        # 1️⃣ Authentication
        auth_response = requests.post(
            "https://accept.paymob.com/api/auth/tokens",
            json={"api_key": paymob_api_key}
        ).json()

        if "token" not in auth_response:
            return Response({"step": "auth", "error": auth_response}, status=status.HTTP_400_BAD_REQUEST)
        auth_token = auth_response["token"]

        # 2️⃣ Create Order
        order_response = requests.post(
            "https://accept.paymob.com/api/ecommerce/orders",
            json={
                "auth_token": auth_token,
                "delivery_needed": "false",
                "amount_cents": str(int(amount * 100)),
                "currency": currency,
                "items": []
            }
        ).json()

        if "id" not in order_response:
            return Response({"step": "order", "error": order_response}, status=status.HTTP_400_BAD_REQUEST)
        order_id = order_response["id"]

        # 3️⃣ Generate Payment Key
        payment_key_response = requests.post(
            "https://accept.paymob.com/api/acceptance/payment_keys",
            json={
                "auth_token": auth_token,
                "amount_cents": str(int(amount * 100)),
                "expiration": 3600,
                "order_id": order_id,
                "billing_data": {
                    "apartment": "NA",
                    "email": request.user.email or "test@example.com",
                    "floor": "NA",
                    "first_name": request.user.first_name or "User",
                    "street": "NA",
                    "building": "NA",
                    "phone_number": "+201200558476",
                    "shipping_method": "NA",
                    "postal_code": "NA",
                    "city": "Cairo",
                    "country": "EG",
                    "last_name": request.user.last_name or "User",
                    "state": "Cairo"
                },
                "currency": currency,
                "integration_id": integration_id
            }
        ).json()

        if "token" not in payment_key_response:
            return Response({"step": "payment_key", "error": payment_key_response}, status=status.HTTP_400_BAD_REQUEST)

        payment_token = payment_key_response["token"]

        # 4️⃣ Return Payment URL
        payment_url = f"https://accept.paymob.com/api/acceptance/iframes/{iframe_id}?payment_token={payment_token}"
        return Response({"payment_url": payment_url})

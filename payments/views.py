from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings
api_key = settings.PAYMOB_API_KEY

from .models import Payment
from .serializers import PaymentSerializer

class PaymentHistoryView(APIView):
    """
    Payment History API
    """
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
    """
    Stripe Payment API
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process Stripe payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'payment_method_id': openapi.Schema(type=openapi.TYPE_STRING, description='Stripe payment method ID')
            }
        ),
        responses={200: "Payment processed"},
        tags=['Payments']
    )
    def post(self, request):
        # Stripe payment logic will be implemented here
        return Response({'message': 'Stripe payment endpoint - to be implemented'})


class PayPalPaymentView(APIView):
    """
    PayPal Payment API
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process PayPal payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'paypal_order_id': openapi.Schema(type=openapi.TYPE_STRING, description='PayPal order ID')
            }
        ),
        responses={200: "Payment processed"},
        tags=['Payments']
    )
    def post(self, request):
        # PayPal payment logic will be implemented here
        return Response({'message': 'PayPal payment endpoint - to be implemented'})


class PaymobPaymentView(APIView):
    """
    Paymob Payment API
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Process Paymob payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['amount', 'currency', 'paymob_token'],
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_NUMBER, description='Payment amount'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'paymob_token': openapi.Schema(type=openapi.TYPE_STRING, description='Paymob payment token')
            }
        ),
        responses={200: PaymentSerializer},
        tags=['Payments']
    )
    def post(self, request):
        amount = request.data.get('amount')
        currency = request.data.get('currency')
        paymob_token = request.data.get('paymob_token')

        # Basic validation
        if not amount or not currency or not paymob_token:
            return Response(
                {'error': 'Missing required fields: amount, currency, paymob_token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Simulate successful payment (you can integrate with Paymob API here)
        payment = Payment.objects.create(
            user=request.user,
            amount=amount,
            currency=currency,
            provider='Paymob',
            provider_payment_id=paymob_token,  # Assuming paymob_token is used as payment_id
            status='success'  # You can customize this
        )

        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

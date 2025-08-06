from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            'id', 'points_package', 'amount', 'currency', 'payment_method',
            'status', 'external_payment_id', 'created_at', 'completed_at'
        ]

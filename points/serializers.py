from rest_framework import serializers
from django.db import models
from .models import PointsPackage, PointsTransaction, Order
from accounts.serializers import UserProfileSerializer
from skills.serializers import SkillListSerializer

class PointsPackageSerializer(serializers.ModelSerializer):
    discounted_price = serializers.ReadOnlyField()

    class Meta:
        model = PointsPackage
        fields = [
            'id', 'name', 'name_ar', 'points', 'price', 'currency',
            'discount_percentage', 'discounted_price', 'is_popular', 'created_at'
        ]

class PointsTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsTransaction
        fields = [
            'id', 'transaction_type', 'amount', 'status', 'description',
            'balance_before', 'balance_after', 'created_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    buyer = UserProfileSerializer(read_only=True)
    seller = UserProfileSerializer(read_only=True)
    skill = SkillListSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'buyer', 'seller', 'skill', 'points_amount', 'platform_fee',
            'total_points', 'status', 'requirements', 'delivery_notes',
            'created_at', 'accepted_at', 'completed_at', 'expected_delivery'
        ]

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['skill', 'requirements']

    def create(self, validated_data):
        skill = validated_data['skill']
        validated_data['seller'] = skill.user
        validated_data['points_amount'] = skill.points_required
        return super().create(validated_data)

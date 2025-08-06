from rest_framework import serializers
from .models import Review
from accounts.serializers import UserProfileSerializer

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)
    reviewee = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'reviewer', 'reviewee', 'skill', 'order', 'rating',
            'comment', 'communication_rating', 'quality_rating',
            'delivery_rating', 'is_public', 'created_at'
        ]

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'skill', 'order', 'rating', 'comment', 'communication_rating',
            'quality_rating', 'delivery_rating', 'is_public'
        ]

    def create(self, validated_data):
        order = validated_data['order']
        validated_data['reviewee'] = order.seller
        return super().create(validated_data)

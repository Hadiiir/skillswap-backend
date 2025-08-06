from rest_framework import serializers
from .models import Category, Skill, SkillImage, SkillFAQ
from accounts.serializers import UserProfileSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'name_ar', 'description', 'description_ar', 'icon', 'is_active']

class SkillImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillImage
        fields = ['id', 'image', 'caption', 'order']

class SkillFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillFAQ
        fields = ['id', 'question', 'question_ar', 'answer', 'answer_ar', 'order']

class SkillListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags_list = serializers.ReadOnlyField(source='get_tags_list')

    class Meta:
        model = Skill
        fields = [
            'id', 'user', 'category', 'title', 'title_ar', 'description',
            'points_required', 'estimated_duration', 'language', 'difficulty',
            'thumbnail', 'status', 'is_featured', 'total_orders',
            'average_rating', 'total_reviews', 'tags_list', 'created_at'
        ]

class SkillDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = SkillImageSerializer(many=True, read_only=True)
    faqs = SkillFAQSerializer(many=True, read_only=True)
    tags_list = serializers.ReadOnlyField(source='get_tags_list')

    class Meta:
        model = Skill
        fields = [
            'id', 'user', 'category', 'title', 'title_ar', 'description',
            'description_ar', 'points_required', 'estimated_duration',
            'language', 'difficulty', 'thumbnail', 'video_intro',
            'status', 'is_featured', 'total_orders', 'average_rating',
            'total_reviews', 'tags', 'tags_list', 'meta_description',
            'images', 'faqs', 'created_at', 'updated_at'
        ]

class SkillCreateUpdateSerializer(serializers.ModelSerializer):
    images = SkillImageSerializer(many=True, read_only=True)
    faqs = SkillFAQSerializer(many=True, read_only=True)

    class Meta:
        model = Skill
        fields = [
            'category', 'title', 'title_ar', 'description', 'description_ar',
            'points_required', 'estimated_duration', 'language', 'difficulty',
            'thumbnail', 'video_intro', 'tags', 'meta_description', 'images', 'faqs'
        ]

    def validate_points_required(self, value):
        if value < 1:
            raise serializers.ValidationError("Points required must be at least 1")
        if value > 10000:
            raise serializers.ValidationError("Points required cannot exceed 10,000")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

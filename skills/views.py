from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Category, Skill
from .serializers import (
    CategorySerializer, SkillListSerializer, 
    SkillDetailSerializer, SkillCreateUpdateSerializer
)

class SkillFilter(django_filters.FilterSet):
    """Custom filter for skills with more options"""
    category = django_filters.NumberFilter(field_name='category__id')
    category_name = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    language = django_filters.ChoiceFilter(choices=Skill.LANGUAGE_CHOICES)
    difficulty = django_filters.ChoiceFilter(choices=Skill.DIFFICULTY_CHOICES)
    points_min = django_filters.NumberFilter(field_name='points_required', lookup_expr='gte')
    points_max = django_filters.NumberFilter(field_name='points_required', lookup_expr='lte')
    rating_min = django_filters.NumberFilter(field_name='average_rating', lookup_expr='gte')
    rating_max = django_filters.NumberFilter(field_name='average_rating', lookup_expr='lte')
    is_featured = django_filters.BooleanFilter()
    
    class Meta:
        model = Skill
        fields = {
            'category': ['exact'],
            'language': ['exact'],
            'difficulty': ['exact'],
            'points_required': ['exact', 'gte', 'lte'],
            'average_rating': ['gte', 'lte'],
            'is_featured': ['exact'],
            'status': ['exact'],
        }

class CategoryListView(APIView):
    """
    Categories List API
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get all categories",
        responses={200: CategorySerializer(many=True)},
        tags=['Categories']
    )
    def get(self, request):
        categories = Category.objects.filter(is_active=True)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryDetailView(APIView):
    """
    Category Detail API
    """
    permission_classes = [permissions.AllowAny]
    
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk, is_active=True)
        except Category.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Get category detail",
        responses={200: CategorySerializer},
        tags=['Categories']
    )
    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CategorySerializer(category)
        return Response(serializer.data)

class SkillListCreateView(APIView):
    """
    Skills List and Create API
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def apply_filters(self, queryset, request):
        """Apply filters to queryset"""
        # Search
        search = request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title_ar__icontains=search) |
                Q(description__icontains=search) |
                Q(description_ar__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Category filter
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        # Language filter
        language = request.query_params.get('language')
        if language:
            queryset = queryset.filter(language=language)
        
        # Difficulty filter
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        
        # Points range
        points_min = request.query_params.get('points_min')
        if points_min:
            queryset = queryset.filter(points_required__gte=points_min)
        
        points_max = request.query_params.get('points_max')
        if points_max:
            queryset = queryset.filter(points_required__lte=points_max)
        
        # Rating range
        rating_min = request.query_params.get('rating_min')
        if rating_min:
            queryset = queryset.filter(average_rating__gte=rating_min)
        
        rating_max = request.query_params.get('rating_max')
        if rating_max:
            queryset = queryset.filter(average_rating__lte=rating_max)
        
        # Featured filter
        is_featured = request.query_params.get('is_featured')
        if is_featured:
            queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
        
        # Ordering
        ordering = request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset
    
    @swagger_auto_schema(
        operation_description="Get all skills with filtering and search",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title, description, tags", type=openapi.TYPE_STRING),
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter by category ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('language', openapi.IN_QUERY, description="Filter by language", type=openapi.TYPE_STRING),
            openapi.Parameter('difficulty', openapi.IN_QUERY, description="Filter by difficulty", type=openapi.TYPE_STRING),
            openapi.Parameter('points_min', openapi.IN_QUERY, description="Minimum points required", type=openapi.TYPE_INTEGER),
            openapi.Parameter('points_max', openapi.IN_QUERY, description="Maximum points required", type=openapi.TYPE_INTEGER),
            openapi.Parameter('rating_min', openapi.IN_QUERY, description="Minimum rating", type=openapi.TYPE_NUMBER),
            openapi.Parameter('rating_max', openapi.IN_QUERY, description="Maximum rating", type=openapi.TYPE_NUMBER),
            openapi.Parameter('is_featured', openapi.IN_QUERY, description="Filter featured skills", type=openapi.TYPE_BOOLEAN),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Order by field", type=openapi.TYPE_STRING),
        ],
        responses={200: SkillListSerializer(many=True)},
        tags=['Skills']
    )
    def get(self, request):
        try:
            queryset = Skill.objects.filter(status='active').select_related('user', 'category')
            queryset = self.apply_filters(queryset, request)
            
            serializer = SkillListSerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': f'Filter error: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @swagger_auto_schema(
        operation_description="Create a new skill",
        request_body=SkillCreateUpdateSerializer,
        responses={201: SkillDetailSerializer},
        tags=['Skills']
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = SkillCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            skill = serializer.save(user=request.user)
            return Response(SkillDetailSerializer(skill).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SkillDetailView(APIView):
    """
    Skill Detail API
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Skill.objects.select_related('user', 'category').get(pk=pk, status='active')
        except Skill.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Get skill detail",
        responses={200: SkillDetailSerializer},
        tags=['Skills']
    )
    def get(self, request, pk):
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = SkillDetailSerializer(skill)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update skill",
        request_body=SkillCreateUpdateSerializer,
        responses={200: SkillDetailSerializer},
        tags=['Skills']
    )
    def put(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if skill.user != request.user:
            return Response({'error': 'You can only update your own skills'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SkillCreateUpdateSerializer(skill, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(SkillDetailSerializer(skill).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Partially update skill",
        request_body=SkillCreateUpdateSerializer,
        responses={200: SkillDetailSerializer},
        tags=['Skills']
    )
    def patch(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if skill.user != request.user:
            return Response({'error': 'You can only update your own skills'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = SkillCreateUpdateSerializer(skill, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(SkillDetailSerializer(skill).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete skill",
        responses={204: "No Content"},
        tags=['Skills']
    )
    def delete(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
        
        skill = self.get_object(pk)
        if not skill:
            return Response({'error': 'Skill not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if skill.user != request.user:
            return Response({'error': 'You can only delete your own skills'}, status=status.HTTP_403_FORBIDDEN)
        
        skill.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

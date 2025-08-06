from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer

class ReviewListCreateView(APIView):
    """
    Reviews List and Create API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get user's reviews",
        responses={200: ReviewSerializer(many=True)},
        tags=['Reviews']
    )
    def get(self, request):
        reviews = Review.objects.filter(reviewer=request.user)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new review",
        request_body=ReviewCreateSerializer,
        responses={201: ReviewSerializer},
        tags=['Reviews']
    )
    def post(self, request):
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(reviewer=request.user)
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    """
    Review Detail API
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return Review.objects.get(pk=pk, reviewer=user)
        except Review.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        operation_description="Get review detail",
        responses={200: ReviewSerializer},
        tags=['Reviews']
    )
    def get(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Update review",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer},
        tags=['Reviews']
    )
    def put(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Partially update review",
        request_body=ReviewSerializer,
        responses={200: ReviewSerializer},
        tags=['Reviews']
    )
    def patch(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete review",
        responses={204: "No Content"},
        tags=['Reviews']
    )
    def delete(self, request, pk):
        review = self.get_object(pk, request.user)
        if not review:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
        
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SkillReviewsView(APIView):
    """
    Skill Reviews API
    """
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(
        operation_description="Get reviews for a specific skill",
        responses={200: ReviewSerializer(many=True)},
        tags=['Reviews']
    )
    def get(self, request, skill_id):
        reviews = Review.objects.filter(skill_id=skill_id, is_public=True)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

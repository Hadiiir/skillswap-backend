from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db import models
from drf_yasg.utils import swagger_auto_schema
from .models import PointsPackage, PointsTransaction, Order
from .serializers import (
    PointsPackageSerializer, PointsTransactionSerializer,
    OrderSerializer, OrderCreateSerializer
)

# ---------------------------
# قائمة باكدجات النقاط المتاحة
# ---------------------------
class PointsPackageListView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Get all available points packages",
        responses={200: PointsPackageSerializer(many=True)},
        tags=['Points']
    )
    def get(self, request):
        packages = PointsPackage.objects.filter(is_active=True)
        serializer = PointsPackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------------------
# قائمة معاملات النقاط للمستخدم
# ---------------------------
class PointsTransactionListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user's points transactions",
        responses={200: PointsTransactionSerializer(many=True)},
        tags=['Points']
    )
    def get(self, request):
        transactions = PointsTransaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = PointsTransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------------------
# قائمة الطلبات + إنشاء طلب جديد
# ---------------------------
class OrderListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get user's orders (as buyer or seller)",
        responses={200: OrderSerializer(many=True)},
        tags=['Orders']
    )
    def get(self, request):
        orders = Order.objects.filter(
            models.Q(buyer=request.user) | models.Q(seller=request.user)
        ).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new order",
        request_body=OrderCreateSerializer,
        responses={201: OrderSerializer},
        tags=['Orders']
    )
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(buyer=request.user)
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------
# تفاصيل طلب معين
# ---------------------------
class OrderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get order detail",
        responses={200: OrderSerializer},
        tags=['Orders']
    )
    def get(self, request, pk):
        try:
            order = Order.objects.filter(
                models.Q(buyer=request.user) | models.Q(seller=request.user)
            ).get(pk=pk)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------------------
# قبول الطلب (من قبل البائع فقط)
# ---------------------------
class AcceptOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Accept an order (seller only)",
        responses={200: "Order accepted"},
        tags=['Orders']
    )
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, seller=request.user, status='pending')
            order.status = 'accepted'
            order.accepted_at = timezone.now()
            order.save()
            return Response({'status': 'Order accepted'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or not pending'}, status=status.HTTP_404_NOT_FOUND)

# ---------------------------
# إكمال الطلب (من قبل البائع فقط)
# ---------------------------
class CompleteOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Complete an order (seller only)",
        responses={200: "Order completed"},
        tags=['Orders']
    )
    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk, seller=request.user, status='in_progress')
            order.status = 'completed'
            order.completed_at = timezone.now()
            order.save()
            return Response({'status': 'Order completed'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found or not in progress'}, status=status.HTTP_404_NOT_FOUND)

# ---------------------------
# إلغاء الطلب (من قبل المشتري أو البائع)
# ---------------------------
class CancelOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Cancel an order (buyer or seller)",
        responses={200: "Order cancelled"},
        tags=['Orders']
    )
    def post(self, request, pk):
        try:
            order = Order.objects.filter(
                models.Q(buyer=request.user) | models.Q(seller=request.user)
            ).get(pk=pk)

            order.status = 'cancelled'
            order.cancelled_at = timezone.now()
            order.save()
            return Response({'status': 'Order cancelled'}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Driver, Order, Poster, Feedback
from .serializers import (
    UserProfileSerializer, DriverSerializer, OrderSerializer,
    PosterSerializer, FeedbackSerializer
)
from django.contrib.auth.models import User
from rest_framework import serializers

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Driver.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get'])
    def active_orders(self, request, pk=None):
        driver = self.get_object()
        orders = Order.objects.filter(driver=driver, status='pending')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'driver'):
            return Order.objects.filter(driver__user=user) | Order.objects.filter(user=user)
        return Order.objects.filter(user=user)

    @action(detail=True, methods=['post'])
    def complete_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'error': 'Order is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'completed'
        order.save()
        return Response({'status': 'Order completed'})

    @action(detail=True, methods=['post'])
    def cancel_order(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'error': 'Order is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'canceled'
        order.save()
        return Response({'status': 'Order canceled'})

class PosterViewSet(viewsets.ModelViewSet):
    queryset = Poster.objects.all()
    serializer_class = PosterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Poster.objects.filter(is_active=True)
        from_location = self.request.query_params.get('from_location')
        to_location = self.request.query_params.get('to_location')
        
        if from_location:
            queryset = queryset.filter(from_location__icontains=from_location)
        if to_location:
            queryset = queryset.filter(to_location__icontains=to_location)
        return queryset

    def perform_create(self, serializer):
        if not hasattr(self.request.user, 'driver'):
            raise serializers.ValidationError("Only drivers can create posters")
        serializer.save(driver=self.request.user.driver)

    @action(detail=False, methods=['get'])
    def available_rides(self, request):
        tomorrow = timezone.now() + timedelta(days=1)
        posters = Poster.objects.filter(
            is_active=True,
            creation_date__lte=tomorrow
        )
        serializer = self.get_serializer(posters, many=True)
        return Response(serializer.data)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
        order = serializer.validated_data['order']
        if order.user != self.request.user:
            raise serializers.ValidationError("You can only give feedback for your own orders")
        serializer.save()
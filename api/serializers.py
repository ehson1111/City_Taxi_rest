from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Driver, Order, Poster, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'rating', 'registration_date']
        read_only_fields = ['registration_date']

class DriverSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Driver
        fields = ['id', 'user', 'car_model', 'car_number', 'car_photo']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    driver = DriverSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'driver', 'pickup', 'destination', 
                 'status', 'order_date']
        read_only_fields = ['order_date']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PosterSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    
    class Meta:
        model = Poster
        fields = ['id', 'from_location', 'to_location', 'price', 
                 'time_to_go', 'bags', 'driver', 'is_active', 'creation_date']
        read_only_fields = ['creation_date']

class FeedbackSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    
    class Meta:
        model = Feedback
        fields = ['id', 'order', 'rating', 'comment', 'date']
        read_only_fields = ['date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value
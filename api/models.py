from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    rating = models.FloatField(default=5.0)
    registration_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=100)
    car_number = models.CharField(max_length=20)
    car_photo = models.ImageField(upload_to='car_photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.car_model}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup = models.CharField(max_length=100)
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    destination = models.CharField(max_length=100)
    destination_latitude = models.FloatField(null=True, blank=True)
    destination_longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} - {self.pickup} to {self.destination}"

class Poster(models.Model):
    from_location = models.CharField(max_length=100)
    from_latitude = models.FloatField(null=True, blank=True)
    from_longitude = models.FloatField(null=True, blank=True)
    to_location = models.CharField(max_length=100)
    to_latitude = models.FloatField(null=True, blank=True)
    to_longitude = models.FloatField(null=True, blank=True)
    price = models.FloatField()
    time_to_go = models.CharField(max_length=10)
    bags = models.IntegerField()
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.from_location} to {self.to_location}"

class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feedback for Order #{self.order.id}"
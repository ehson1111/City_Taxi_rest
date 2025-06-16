from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, DriverViewSet, OrderViewSet, PosterViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'drivers', DriverViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'posters', PosterViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
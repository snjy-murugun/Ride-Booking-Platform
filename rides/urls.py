from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, RideViewSet, TripLogViewSet, PaymentViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'rides', RideViewSet)
router.register(r'triplogs', TripLogViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

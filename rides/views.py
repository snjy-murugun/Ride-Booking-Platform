from rest_framework import viewsets
from .models import Vehicle, Ride, TripLog, Payment, Review
from .serializers import VehicleSerializer, RideSerializer, TripLogSerializer, PaymentSerializer, ReviewSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer

class TripLogViewSet(viewsets.ModelViewSet):
    queryset = TripLog.objects.all()
    serializer_class = TripLogSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

from rest_framework import viewsets
from .models import Vehicle, Ride, TripLog, Payment, Review
from .serializers import VehicleSerializer, RideSerializer, TripLogSerializer, PaymentSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRiderOrAdmin, IsDriverOrAdmin, IsAdmin


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsDriverOrAdmin()]

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsRiderOrAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsDriverOrAdmin()]
        return [IsAuthenticated()]

class TripLogViewSet(viewsets.ModelViewSet):
    queryset = TripLog.objects.all()
    serializer_class = TripLogSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsDriverOrAdmin()]
        return [IsAuthenticated()]
    

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [IsRiderOrAdmin()]
        return [IsAuthenticated()]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsRiderOrAdmin()]
        return [IsAuthenticated()]
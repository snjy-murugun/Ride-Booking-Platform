from rest_framework import viewsets
from .models import Vehicle, Ride, TripLog, Payment, Review
from .serializers import VehicleSerializer, RideSerializer, TripLogSerializer, PaymentSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRiderOrAdmin, IsDriverOrAdmin, IsAdmin
from rest_framework.decorators import action
from rest_framework import status 
from rest_framework.response import Response


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
    
    def perform_create(self, serializer):
        
        review = serializer.save(reviewer=self.request.user)

        ride = review.ride
        if ride.status != 'reviewed':
            ride.status = 'reviewed'
            ride.save()
    
    # custom mini api named status for triplife cycle
    @action(detail=True, methods=['patch'], url_path='status')
    def change_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get('status')

        allowed_status = ['accepted', 'started', 'completed', 'cancelled']
        if new_status not in allowed_status:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = new_status
        ride.save()

        return Response({
            "message": f"Ride status updated to {new_status}.",
            "ride_id": ride.id,
            "status": ride.status
        }, status=status.HTTP_200_OK)


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
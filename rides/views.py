from rest_framework import viewsets
from .models import Vehicle, Ride, TripLog, Payment, Review
from .serializers import VehicleSerializer, RideSerializer, TripLogSerializer, PaymentSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRiderOrAdmin, IsDriverOrAdmin, IsAdmin
from rest_framework.decorators import action
from rest_framework import status 
from rest_framework.response import Response
from django.utils import timezone 
from rest_framework import serializers 


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
        
        ride = serializer.save()
        vehicle_type = ride.vehicle.vehicle_type if ride.vehicle else 'car'
        waiting_time = 0
        from .models import calculate_estimated_fare
        fare = calculate_estimated_fare(vehicle_type, ride.distance_km, waiting_time)
        ride.estimated_fare = fare
        ride.save()
        
        
        #finds nearest available driver
        
        from users.models import user
        available_driver = user.objects.filter(role='driver', is_available=True).first()

        if available_driver:
            ride.driver = available_driver
            ride.status = 'accepted'  

           
            from rides.models import Vehicle
            assigned_vehicle = Vehicle.objects.filter(driver=available_driver).first()
            if assigned_vehicle:
                ride.vehicle = assigned_vehicle

            # Step 4: Mark driver unavailable
            available_driver.is_available = False
            available_driver.save()
        else:
            ride.status = 'requested'  

        ride.save()
        
        
    
    # preview fare estimation endpoint
    
    @action(detail=False, methods=['post'], url_path='fare-estimate')
    
    def fare_estimate(self, request):
        
        from .models import calculate_estimated_fare  

        
        vehicle_type = request.data.get('vehicle_type')
        vehicle_id = request.data.get('vehicle')
        distance_km = request.data.get('distance_km')
        waiting_minutes = float(request.data.get('waiting_minutes', 0))

        
        if not distance_km:
            return Response({'error': 'distance_km is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            distance_km = float(distance_km)
        except ValueError:
            return Response({'error': 'distance_km must be a number.'}, status=status.HTTP_400_BAD_REQUEST)

        
        if vehicle_id:
            try:
                vehicle_obj = Vehicle.objects.get(pk=vehicle_id)
                vehicle_type = vehicle_obj.vehicle_type
            except Vehicle.DoesNotExist:
                return Response({'error': 'Vehicle not found.'}, status=status.HTTP_404_NOT_FOUND)

    
        if not vehicle_type:
            vehicle_type = 'car'


        estimated_fare = calculate_estimated_fare(vehicle_type, distance_km, waiting_minutes)


        return Response({
            "message": "Fare estimated successfully.",
            "estimated_fare": estimated_fare,
            "details": {
                "vehicle_type": vehicle_type,
                "distance_km": distance_km,
                "waiting_minutes": waiting_minutes
            }
        }, status=status.HTTP_200_OK)

    # custom mini api named status for triplife cycle
    
    @action(detail=True, methods=['patch'], url_path='status')
    
    def change_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get('status')

        allowed_status = ['accepted', 'started', 'completed', 'cancelled']
        if new_status not in allowed_status:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        
        # accepted

        if new_status == 'accepted':
            ride.status = 'accepted'
            ride.save()
            return Response({"message": "Ride accepted successfully!"}, status=status.HTTP_200_OK)
        
        # statrted

        elif new_status == 'started':
            ride.status = 'started'
            ride.save()

            TripLog.objects.create(
                ride=ride,
                start_time=timezone.now(),
                route_data={"message": "Trip started from source"}
            )

            return Response({
                "message": "Ride started! TripLog created.",
                "ride_id": ride.id
            }, status=status.HTTP_200_OK)

        # completed 
        
        elif new_status == 'completed':
            ride.status = 'completed'
            ride.save()

            trip_log = getattr(ride, 'trip_log', None)
            if trip_log:
                trip_log.end_time = timezone.now()
                # calculate duration in minutes
                trip_log.duration_minutes = (trip_log.end_time - trip_log.start_time).total_seconds() / 60
                trip_log.save()


            Payment.objects.create(
                ride=ride,
                user=ride.rider,
                amount=ride.estimated_fare, 
                method='cash',
                status='pending'
            )
            
            
            # if the driver is completed, and still online, mark them available again
            
            if ride.driver:
                ride.driver.is_available = True
                ride.driver.save()


            return Response({
                "message": "Ride completed! TripLog updated and Payment created.",
                "ride_id": ride.id,
                "trip_duration_mins": trip_log.duration_minutes if trip_log else None
            }, status=status.HTTP_200_OK)

        # cancelled
        
        elif new_status == 'cancelled':
            ride.status = 'cancelled'
            ride.save()
            return Response({"message": "Ride cancelled."}, status=status.HTTP_200_OK)


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
    
    def perform_create(self, serializer):
        
        ride = serializer.validated_data.get('ride')
        
        if ride.status != 'completed':
            raise serializers.ValidationError({'ride': ["Cannot review a ride that is not completed."]})
        
        review = serializer.save()
    
        ride = review.ride
        if ride.status != 'reviewed':
            ride.status = 'reviewed'
            ride.save()
            
        
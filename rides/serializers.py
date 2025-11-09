from rest_framework import serializers
from rides.models import Ride, Vehicle, TripLog, Payment, Review

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    ride_status = serializers.CharField(source='ride.status', read_only=True)
    class Meta:
        model = Ride
        fields = '__all__'
        extra_fields = ['rider_status']

class TripLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripLog
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
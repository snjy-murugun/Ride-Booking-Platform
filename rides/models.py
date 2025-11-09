from django.db import models
from django.conf import settings
from users.models import user

class Vehicle(models.Model):                                     
    driver = models.ForeignKey(                                  
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'driver'}
    )
    vehicle_number = models.CharField(max_length=20, unique=True) 
    model_name = models.CharField(max_length=50)                  
    vehicle_type = models.CharField(                              
        max_length=20,
        choices=[
            ('car', 'Car'),
            ('bike', 'Bike'),
            ('auto', 'Auto'),
        ],
        default='car'
    )
    capacity = models.PositiveIntegerField(default=4)            
    is_active = models.BooleanField(default=True)                 

    def __str__(self):                                            
        return f"{self.model_name} - {self.vehicle_number}"
    

class Ride(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rider_rides', limit_choices_to={'role': 'rider'})
    
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='driver_rides', limit_choices_to={'role': 'driver'}, null=True, blank=True) 
    
    vehicle = models.ForeignKey('rides.vehicle', on_delete=models.SET_NULL, null=True, blank=True)
    
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    distance_km = models.FloatField(default=0.0)
    estimated_fare = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),    
        ('reviewed', 'Reviewed'),
    ]
    
    status = models.CharField(max_length=20, choices = STATUS_CHOICES, default='requested')   
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)    
    
    def _str_(self):
        return f"{self.rider.username} -> {self.destination} ({self.status}) "
    
    

class TripLog(models.Model):                                         
    ride = models.OneToOneField(                                    
        'rides.Ride',
        on_delete=models.CASCADE,
        related_name='trip_log'
    )
    start_time = models.DateTimeField(null=True, blank=True)         
    end_time = models.DateTimeField(null=True, blank=True)            
    duration_minutes = models.FloatField(default=0.0)                 
    route_data = models.JSONField(default=dict, blank=True)          
    created_at = models.DateTimeField(auto_now_add=True)              

    def __str__(self):                                                
        return f"TripLog for Ride ID {self.ride.id}"


class Payment(models.Model):                                        
    ride = models.OneToOneField(                                    
        'rides.Ride',
        on_delete=models.CASCADE,
        related_name='payment'
    )
    user = models.ForeignKey(                                        
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    amount = models.DecimalField(                                   
        max_digits=8,
        decimal_places=2
    )
    method = models.CharField(                                      
        max_length=20,
        choices=[
            ('cash', 'Cash'),
            ('upi', 'UPI'),
            ('card', 'Card'),
        ],
        default='cash'
    )
    status = models.CharField(                                       
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('successful', 'Successful'),
            ('failed', 'Failed'),
        ],
        default='pending'
    )
    transaction_id = models.CharField(                               
        max_length=100,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)             

    def __str__(self):                                               
        return f"Payment for Ride {self.ride.id} - {self.status}"



class Review(models.Model):                                  
    ride = models.OneToOneField(                                   
        'rides.Ride',
        on_delete=models.CASCADE,
        related_name='review'
    )
    rider = models.ForeignKey(                                      
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        limit_choices_to={'role': 'rider'}
    )
    driver = models.ForeignKey(                                     
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        limit_choices_to={'role': 'driver'}
    )
    rating = models.PositiveSmallIntegerField(                      
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5
    )
    comment = models.TextField(blank=True, null=True)               
    created_at = models.DateTimeField(auto_now_add=True)           

    def __str__(self):                                              
        return f"Review for Ride {self.ride.id} - {self.rating} Stars"

# helper function 

from datetime import datetime, time

def calculate_estimated_fare(vehicle_type, distance_km, waiting_time=0):
    
    
    base_fare = 50
    waiting_charge_per_min = 5

    per_km_rates = {
        'car': 15,
        'auto': 12,
        'bike': 10
    }
    per_km_rate = per_km_rates.get(vehicle_type, 10)

    # base fare
    total_fare = base_fare + (distance_km * per_km_rate) + (waiting_time * waiting_charge_per_min)

    #peak hour
    current_time = datetime.now().time()
    peak_hours = [(time(8, 0), time(10, 0)), (time(17, 0), time(20, 0))]  # 8–10 AM, 5–8 PM
    for start, end in peak_hours:
        if start <= current_time <= end:
            total_fare *= 1.5  # 50% increase during peak
            break

    return round(total_fare, 2)

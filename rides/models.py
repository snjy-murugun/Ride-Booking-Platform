from django.db import models
from django.conf import settings

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
        ('reviewd', 'Reviewed'),
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

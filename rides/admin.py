
# Register your models here.
from django.contrib import admin
from .models import Vehicle
from .models import Ride
from .models import TripLog 
from .models import Payment 
from .models import Review 


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'driver', 'model_name', 'vehicle_type', 'is_active')

@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'driver', 'status', 'estimated_fare', 'created_at')
    list_filter = ('status',)
    search_fields = ('rider__username', 'driver__username', 'destination')
    
@admin.register(TripLog)
class TripLogAdmin(admin.ModelAdmin):
    list_display = ('ride', 'start_time', 'end_time', 'duration_minutes', 'created_at')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ride', 'user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('status', 'method')
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ride', 'rider', 'driver', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('rider__username', 'driver__username')
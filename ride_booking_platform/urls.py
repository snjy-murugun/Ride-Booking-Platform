"""
URL configuration for ride_booking_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from frontend import views as frontend_views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,    
    TokenRefreshView,)

urlpatterns = [
    path('', frontend_views.home, name='home'),
    path('rider/dashboard/', frontend_views.rider_dashboard, name='rider_dashboard'),
    path('driver/dashboard/', frontend_views.driver_dashboard, name='driver_dashboard'),
    path('admin/panel/', frontend_views.admin_panel, name='admin_panel'),
    path('login/', frontend_views.login_page, name='login'),
    path('signup/', frontend_views.signup_page, name='signup'),
    path('admin/', admin.site.urls),
    path('api/', include('rides.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

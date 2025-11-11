from django.shortcuts import render

# Create your views here.


def home(request):
    
    return render(request, 'frontend/index.html')


def rider_dashboard(request):
    
    return render(request, 'frontend/rider_dashboard.html')


def driver_dashboard(request):

    return render(request, 'frontend/driver_dashboard.html')

def admin_panel(request):
    
    return render(request, 'frontend/admin_panel.html')


def login_page(request):

    return render(request, 'frontend/login.html')


def signup_page(request):

    return render(request, 'frontend/signup.html')

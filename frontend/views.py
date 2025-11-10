from django.shortcuts import render

# Create your views here.


def home(request):
    
    """
    This function handles requests for the homepage.
    It simply renders the HTML file: frontend/index.html
    """
    return render(request, 'frontend/index.html')

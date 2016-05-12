from django.shortcuts import render

# Create your views here.
def homepage(request):
    # View code here...
    return render(request, 'home.html')

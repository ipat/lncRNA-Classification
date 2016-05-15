from django.shortcuts import render

# Create your views here.
def homepage(request):
    if request.method == 'POST': # If the form has been submitted...
        print request.POST.get('search-rna')
        try :
            s.connect((host, port))
        except :
            print 'Unable to connect'
     
    return render(request, 'home.html')

from django.shortcuts import render
from django.http import HttpResponse
# from utils import everything
# Create your views here.
def home(request):
    return render(request, 'base/home.html')

def youtoob(request):
    print("this is a simple response")
    print(request.GET['ytInput'])
    # return HttpResponse("""everything.printURL(request.GET['ytInput'])
    return render(request, 'base/home.html', {'ytOutput':request.GET['ytInput']})

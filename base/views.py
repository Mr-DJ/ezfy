from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from utils import controller

# Create your views here.
def home(request):
    if not 'loggedIn' in request.session:
        request.session['loggedIn'] = False
        
    return render(request, 'base/home.html',{'loggedIn': controller.logState(request.session['loggedIn'])})

def convert(request):
    print(request.GET['ytInput'])
    # request.session['convertURI'] = request.GET['ytInput']
    return render(request, 'base/home.html', {'ytOutput':controller.start_conversion(request.GET['ytInput']), 'loggedIn': controller.logState(request.session['loggedIn'])})

def login(request): 
    controller.login()
    if controller.login != '':
        request.session['loggedIn'] = True 
    return redirect('/')
    

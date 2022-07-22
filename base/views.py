from urllib import response
from django.shortcuts import redirect, render
from django.http import HttpResponse
from utils import controller
import json

# Create your views here.
def home(request):
    if not 'loggedIn' in request.session:
        request.session['loggedIn'] = False
        
    return render(request, 'base/home.html',{'loggedIn': controller.logState(request.session['loggedIn'])})

def convert(request):
    controller.login()
    print(request.GET['ytInput'])
    # request.session['convertURI'] = request.GET['ytInput']
    migrate = controller.migrate()
    result = migrate.start_conversion(request.GET['ytInput'])
    if(migrate.c_type == 'sp2yt'):
        result = json.loads(result)
    return render(request, 'base/home.html', {'ytOutput': result, 'loggedIn': controller.logState(request.session['loggedIn']), 'c_type': migrate.c_type})

def login(request): 
    controller.login()
    if controller.login != '':
        request.session['loggedIn'] = True 
    return redirect('/')


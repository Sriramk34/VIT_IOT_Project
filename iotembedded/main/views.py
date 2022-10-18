from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, response

# Create your views here.
def checklogin(request):
    try:
        if request.session["_auth_user_id"] != None:
            return 1
        else:
            return 0
    except:
        return 0

def empty(request):
    return HttpResponseRedirect('index/')

def loginout(request):
    if checklogin(request) == 1:
            logout(request)
            return render(request, 'main/login.html')

    if request.method == 'POST':
        usern = str(request.POST['username'])
        pwd = str(request.POST['password'])
        print("Hello " + usern)
        user = authenticate(username = usern, password = pwd)
        if user is not None:
            login(request, user)
            #print(request.session["_auth_user_id"])
        else:
            return HttpResponse("<h2>Please Check your Username or Password</h2>")
        return HttpResponseRedirect("/index/")
    else:
        return render(request, 'main/login.html')

def index(request):
    if checklogin(request) == 1:
        return HttpResponse("<h2>Index.html</h2>")
    else:
        return HttpResponseRedirect("/login")
        #return render(request, 'main/index.html')
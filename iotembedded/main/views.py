from http import client
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, response
from .models import userDetails, device
from paho.mqtt import client as mqtt_client
import random
# Create your views here.

connected = None

def checklogin(request):
    try:
        if request.session["_auth_user_id"] != None:
            return 1
        else:
            return 0
    except:
        return 0


def connect_mqtt():
    broker = 'localhost'
    port = 1883
    client_id = f'python-mqtt-{random.randint(0, 1000)}'
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set("abc", "abc")
    client.on_connect = on_connect
    client.connect(broker, port)
    global connected
    connected = client
    return client

def publish( message):
    topic = "python/mqtt"
    msg_count = 0
    msg = message
    global connected
    client = connected
    result = client.publish(topic, msg)
    status = result[0]
        


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
            connect_mqtt()
            #print(request.session["_auth_user_id"])
        else:
            return HttpResponse("<h2>Please Check your Username or Password</h2>")
        return HttpResponseRedirect("/index/")
    else:
        return render(request, 'main/login.html')

def index(request):
    if checklogin(request) == 1:
        userobj = User.objects.get(id = request.session["_auth_user_id"])
        userdet = userDetails.objects.get(user = userobj)
        return render(request, 'main/index.html', {
            "username": userdet.Name
        })
    else:
        return HttpResponseRedirect("/login")
        #return render(request, 'main/index.html')

def control(request):
    if request.method == "POST":
        ID = request.POST['Toggle']
        temp = device.objects.get(deviceID=ID)
        publish(str(temp.deviceStatus))
        temp.deviceStatus = not temp.deviceStatus 
        temp.save()
        
        
    ids = []
    names = []
    st = []
    userobj = User.objects.get(id = request.session["_auth_user_id"])
    userdet = userDetails.objects.get(user = userobj)
    devices = device.objects.filter(DeviceOwner = userdet)
    for i in devices:
        ids.append(i.deviceID)
        names.append(i.deviceName)
        if i.deviceStatus == True:
            st.append("ON")
        else:
            st.append("OFF")
    print(st)
    return render(request, 'main/control.html', {
        "devices":devices
    })

from http import client
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, response
from .models import userDetails, device, sensor
from paho.mqtt import client as mqtt_client
import random
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

connected = None
def jsonparse(a,b, graph):
    res = []
    for i in range(len(a)):
        temp = {}
        if graph == 0:
            temp['x'] = a[i]
        else:
            temp['x'] = i
        temp['y'] = b[i]
        res.append(temp)
    return json.dumps(res, indent=4)


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


def control(request):
    if checklogin(request) == 1:
        if request.method == "POST":
            ID = request.POST['Toggle']
            temp = device.objects.get(deviceID=ID)
            publish(str(temp.deviceID) + "_" + str(temp.deviceStatus))
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
    else:
        return HttpResponseRedirect("/login")

def report(request):
    if checklogin(request):
        if request.method == 'POST':
            if str(request.POST['generate']).lower() == 'update':
                graphtype = 0
                publish("update")
            elif str(request.POST['generate']).lower() == 'scatter':
                graphtype = 1
            else:
                graphtype =0
            userid = User.objects.get(id = request.session["_auth_user_id"])
            name = userid.first_name
            data = list(sensor.objects.filter(UserID = userid).order_by('time'))
            print(data)
            print("Name: " + name)
            a = []
            b = []
            print(data)
            for i in range(len(data)):
                temp = str(data[i].time)
                print(temp)
                a.append(temp[0:16])
                print(a[i])
                b.append(data[i].data)
            j = jsonparse(a,b, graphtype)
            return render(request, 'main/report.html',{
                'data': j, 'type':graphtype, "N":len(a)
            })
        else:
            graphtype = 0
            userid = User.objects.get(id = request.session["_auth_user_id"])
            name = userid.first_name
            data = list(sensor.objects.filter(UserID = userid).order_by('time'))
            print(data)
            print("Name: " + name)
            a = []
            b = []
            print(data)
            for i in range(len(data)):
                temp = str(data[i].time)
                print(temp)
                a.append(temp[0:16])
                print(a[i])
                b.append(data[i].data)
            j = jsonparse(a,b, graphtype)
            return render(request, 'main/report.html',{
                'data': j, 'type':graphtype, "N":len(a)
            })
    else:
        return HttpResponseRedirect("/login")

@csrf_exempt
def temp(request):
    if request.method == 'POST':
        userid = User.objects.get(id = request.POST['ID'])
        s = sensor(UserID = userid,data = request.POST['Data'])
        s.save()
    return render(request, 'main/temp.html')


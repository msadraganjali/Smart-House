import requests
from random import randint

from . import models
from . import models as models
from home.models import GrafData
from home import models as homeModel
from .forms import UserCreationForm2
from api.views import updateAccuWheather
from api.models import AccuWheather, MotionDetectors

from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
from datetime import datetime
from django.contrib.auth import views as auth_views

# fucntion marbot be load profile
@login_required(login_url="login")
def profile(request):
    # gereftan objectha ba queryset ha
    user = request.user
    usage = homeModel.GrafData.objects.all().filter(user=user.uuid)
    home = homeModel.Home.objects.all().filter(user=user.uuid).first()
    is_fire = homeModel.GrafData.objects.all().filter(user=user.uuid).last()
    temp = homeModel.GrafData.objects.filter(user=user.uuid).last()
    hum = homeModel.GrafData.objects.filter(user=user.uuid).last()
    isEarthHum = homeModel.GrafData.objects.filter(user=user.uuid).last()
    motion = homeModel.GrafData.objects.filter(user=user.uuid).last()
    gas = homeModel.GrafData.objects.filter(user=user.uuid).last()
    temp2 = homeModel.GrafData.objects.filter(user=user.uuid).last()
    distance = homeModel.GrafData.objects.filter(user=user.uuid).last()
    
    # accuWheatherValue = updateAccuWheather(request)
    cityTemp = 20.0
    cityStatus = "ابر و خورشید"
    
    if motion:
        motion = motion.motion
    else:
        motion = False
    
    if gas:
        gas = gas.gas
        if gas >= 200:
            gasStatus = True
        else:
            gasStatus = False
    else:
        gas = -1
        gasStatus = False
    
    if distance:
        distance = distance.distance
        if gas >= 200:
            distanceStatus = True
        else:
            distanceStatus = False
    else:
        distance = -1
        gasStatus = False
    

    
    if is_fire:
        is_fire = is_fire.is_fire
    else:
        is_fire = False
    
    if temp:
        temp = temp.temp
    else:
        temp = 0
    
    if temp2:
        temp2 = temp2.temp2
    else:
        temp2 = 0
    
    if hum:
        hum = hum.hum
    else:
        hum = 0
        
    if isEarthHum:
        isEarthHum = isEarthHum.isEarthHum
    else:
        isEarthHum = False
    
    if isEarthHum == False:
        isEarthHum = 1
    elif isEarthHum == True:
        isEarthHum = 0
    
    e_total_usage = []
    w_total_usage = []
    g_total_usage = []
    total_temp = []
    total_hum = []
    total_gas = []
    int_e = 0
    int_w = 0
    int_g = 0
    # halghe dar queryset ha
    for q in usage:
        e_total_usage.append(q.e_usage)
        eq = randint(0, 1)
        if eq:
            w_total_usage.append(randint(q.e_usage + 5 , q.e_usage + 10))
            g_total_usage.append(randint(q.e_usage + 2 , q.e_usage + 5))
        else:
            w_total_usage.append(randint(q.e_usage + 5 , q.e_usage + 5))
            g_total_usage.append(randint(q.e_usage + 2 , q.e_usage + 10))

        total_hum.append(q.hum)
        total_temp.append(q.temp)
        total_gas.append(q.gas)
    for e in e_total_usage:
        int_e += e
    
    for w in w_total_usage:
        int_w += w

    for g in g_total_usage:
        int_g += g
    
    if not home:
        home = None
    # check kardan queryset haye khane
    motion_detected = MotionDetectors.objects.all().filter(user = request.user).first()
    return render(request, 'account/profile.html', {"home": home, "user": user, "usage": usage, "e_total_usage": e_total_usage, "w_total_usage": w_total_usage, "g_total_usage": g_total_usage, "int_e" : int_e, "int_g" : int_g, "int_w" : int_w,"is_fire" : is_fire, "temp" : temp, "total_temp" : total_temp, "isEarthHum":isEarthHum, "hum": hum, "total_hum": total_hum, "motion" : motion, "total_gas" : gas, "gas" : gas, "cityStatus":cityStatus, "cityTemp":cityTemp, 'motion_detected' : motion_detected, "gasStatus" : gasStatus, "temp2":temp2, "distance" : distance})

# klass marbot be register kardan karbar
class RegisterFormView(FormView):
    template_name = "account/register.html"
    form_class = UserCreationForm2
    model = models.User
    success_url = reverse_lazy("login")
    # dar sorati ke form bedone khata az taraf karbar masalan entekhabe ramz obore kootah(nabood)
    def form_valid(self, form):
        user = form.save()
        # packages creation
        nullPackage = homeModel.Package.objects.create(name = "خالی", description="خالی", visible = True, enabled=True, user = user)
        travelPackage = homeModel.Package.objects.create(name = "مسافرت", description="مسافرت", visible = True, enabled=False, user = user)
        exithomePackage = homeModel.Package.objects.create(name = "خروج از منزل", description="خروج از منزل", visible = True, enabled=False, user = user)
        morningPackage = homeModel.Package.objects.create(name = "صبح", description="صبح", visible = True, enabled=False, user = user)
        BabyPackage = homeModel.Package.objects.create(name = "کودک", description="کودک", visible = True, enabled=False, user = user)
        enterHomePackage = homeModel.Package.objects.create(name = "ورود به منزل", description="ورود به منزل", visible = True, enabled=False, user = user)
        # device creation
        livingLamp = homeModel.device.objects.create(name = "living-lamp" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data = 255)
        roomLamp = homeModel.device.objects.create(name = "room-lamp" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data = 255)
        yardLamp = homeModel.device.objects.create(name = "yard-lamp" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data = 255)
        television = homeModel.device.objects.create(name = "television" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        hiter = homeModel.device.objects.create(name = "hiter" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        fanCooler = homeModel.device.objects.create(name = "fanCooler" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        parkingDoor = homeModel.device.objects.create(name = "parkingDoor" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        teaMeacker = homeModel.device.objects.create(name = "teaMeacker" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        flowerWhater = homeModel.device.objects.create(name = "flowerWhater" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        poolWhater = homeModel.device.objects.create(name = "poolWhater" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        animalsFood = homeModel.device.objects.create(name = "animalsFood" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        mainDoor = homeModel.device.objects.create(name = "mainDoor" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        gas = homeModel.device.objects.create(name = "gas" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        windowDoor = homeModel.device.objects.create(name = "windowDoor" , status = 0, user = user, color="red", btn="danger", element="برق", password = 1234, data=255)
        # timeOfDevices creation
        # exit home Package
        homeModel.TimeOfDevice.objects.create(user= user, device_id = livingLamp.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = roomLamp.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = yardLamp.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = television.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = hiter.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = fanCooler.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = parkingDoor.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = teaMeacker.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = flowerWhater.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = poolWhater.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = animalsFood.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  mainDoor.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  gas.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  windowDoor.pk, time = "0:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=exithomePackage.pk)
        # morning Package
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  livingLamp.pk, time = "00:00:00", time2 ="23:59:59", data=40, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = roomLamp.pk, time = "00:00:00", time2 ="23:59:59", data=40, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = yardLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  television.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = hiter.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = fanCooler.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = parkingDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  teaMeacker.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = flowerWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  poolWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  animalsFood.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  mainDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  gas.pk, time = "00:00:00", time2 ="23:59:59",status=1, data=255, isPackMode=True, package_id=morningPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  windowDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=morningPackage.pk)
        # Baby Care Package
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  livingLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  roomLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  yardLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  television.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  hiter.pk, time = "00:00:00", time2 ="23:59:59", data=50, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = fanCooler.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = parkingDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  teaMeacker.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = flowerWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  poolWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  animalsFood.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  mainDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  gas.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=BabyPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  windowDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=BabyPackage.pk)
        # enter to home
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  livingLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  roomLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  yardLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  television.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  hiter.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  fanCooler.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = parkingDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  teaMeacker.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  flowerWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  poolWhater.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  animalsFood.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  mainDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  gas.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=1, isPackMode=True, package_id=enterHomePackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  windowDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=enterHomePackage.pk)
        # travel Package
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  livingLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  roomLamp.pk, time = "00:00:00", time2 ="23:59:59", data=100, status=1, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  yardLamp.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  television.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  hiter.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  fanCooler.pk, time = "00:00:00", time2 ="23:59:59", data=50, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id = parkingDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  teaMeacker.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  flowerWhater.pk, time = "7:00:00", time2 ="7:00:10", data=50, status=1, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  poolWhater.pk, time = "7:00:00", time2 ="7:00:10", data=50, status=1, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  animalsFood.pk, time = "7:00:00", time2 ="7:00:10", data=50, status=1, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  mainDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  gas.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        homeModel.TimeOfDevice.objects.create(user= user, device_id =  windowDoor.pk, time = "00:00:00", time2 ="23:59:59", data=255, status=0, isPackMode=True, package_id=travelPackage.pk)
        # accu Wheader instance creation
        try:
            accuWheader = requests.get("https://dataservice.accuweather.com/currentconditions/v1/208194?apikey=gYcIOAnOquMbLz9GE2kbAFuyh5QQ6ceS&language=fa-ir")
            if accuWheader.status_code == 200:
                responseCity = accuWheader.json()
                cityStatus = responseCity[0]["WeatherText"]
                cityTemp = responseCity[0]["Temperature"]["Metric"]["Value"]
                AccuWheather.objects.create(temp = cityTemp, user = user, status = cityStatus)
            else:
                cityStatus = "دریافت نشده."
                cityTemp = 0.0
                AccuWheather.objects.create(temp = cityTemp, user = user, status = cityStatus)
        except requests.exceptions.ConnectTimeout:
            cityStatus = "دریافت نشده."
            cityTemp = 0.0
            AccuWheather.objects.create(temp = cityTemp, user = user, status = cityStatus)
        except requests.exceptions.ConnectionError:
            cityStatus = "دریافت نشده."
            cityTemp = 0.0
            AccuWheather.objects.create(temp = cityTemp, user = user, status = cityStatus)
        # motionDetector instance creation
        MotionDetectors.objects.create(user = user, status=False)
        homeModel.GrafData.objects.create(user = user, e_usage=0, is_fire=0, temp=0.0, isEarthHum=0, hum=0.0, gas=0, motion=0, temp2 = 0.00, distance = 0)
        return super().form_valid(form)

# fucntion marbot be logout kardan
def logout(request):
    logout(request)
    return render(request, "account/logout.html", {})

class LoginView(auth_views.LoginView):
    template_name = "account/login.html"

class LogoutView(auth_views.LogoutView):
    template_name = "account/logged_out.html"
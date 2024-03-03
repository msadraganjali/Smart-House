import requests
from random import randint

from . import models
from . import models as models
from home.models import GrafData
from home import models as homeModel
from .forms import UserCreationForm2
from api.views import updateAccuWheather

from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView, CreateView
from django.urls import reverse_lazy
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
    
    accuWheatherValue = updateAccuWheather(request)
    cityTemp = accuWheatherValue.temp
    cityStatus = accuWheatherValue.status
    
    if motion:
        motion = motion.motion
    else:
        motion = False
    
    if gas:
        gas = gas.gas
    else:
        gas = 0
        
    if is_fire:
        is_fire = is_fire.is_fire
    else:
        is_fire = False
    
    if temp:
        temp = temp.temp
    else:
        temp = 0
    
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
    return render(request, 'account/profile.html', {"home": home, "user": user, "usage": usage, "e_total_usage": e_total_usage, "w_total_usage": w_total_usage, "g_total_usage": g_total_usage, "int_e" : int_e, "int_g" : int_g, "int_w" : int_w,"is_fire" : is_fire, "temp" : temp, "total_temp" : total_temp, "isEarthHum":isEarthHum, "hum": hum, "total_hum": total_hum, "motion" : motion, "total_gas" : gas, "gas" : gas, "cityStatus":cityStatus, "cityTemp":cityTemp})

# klass marbot be register kardan karbar
class RegisterFormView(FormView):
    template_name = "account/register.html"
    form_class = UserCreationForm2
    model = models.User
    success_url = reverse_lazy("login")
    # dar sorati ke form bedone khata az taraf karbar masalan entekhabe ramz obore kootah(nabood)
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

# fucntion marbot be logout kardan
def logout(request):
    logout(request)
    return render(request, "account/logout.html", {})

class LoginView(auth_views.LoginView):
    template_name = "account/login.html"

class LogoutView(auth_views.LogoutView):
    template_name = "account/logged_out.html"
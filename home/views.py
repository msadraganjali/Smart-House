import requests
from random import randint

from . import forms
from . import models
from api.views import updateAccuWheather
from api.models import MotionDetectors
from home import models as homeModel
# import haye django
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, FormView, ListView

# klas safhe about me
class CreateHomeView(FormView, LoginRequiredMixin):
    template_name = "home/send.html"
    success_url = reverse_lazy("profile")
    form_class =  forms.HomeCreationForm
#   age form bedone khata az taraf karbar bashe bashe...
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

# klas safhe about me
class HomeView(TemplateView):
    template_name = "home/index.html"

# klas safhe about me
class GuideView(TemplateView):
    template_name = "home/guide.html"

# klas safhe about me
class AboutMe(TemplateView):
    template_name = "resume/index.html"

# class CreateDeviceView(CreateView, LoginRequiredMixin):
#     template_name = 'home/send_device.html'
#     form_class = forms.DeviceCreationForm
#     success_url = reverse_lazy('profile')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         form.save()
#         return super().form_valid(form)

def send(request):
    if request.method == 'POST':
        # validation kardan etlaat
        form = forms.DeviceCreationForm(request.POST)

        if not form.is_valid() :
            if form.cleaned_data['element'] == "آب":
                color = "blue"
                btn = "primary"
            elif form.cleaned_data['element'] == "برق":
                color = "red"
                btn = "danger"
            elif form.cleaned_data['element'] == "گاز":
                color = "#FFA500"
                btn = "warning"

            models.device.objects.create(
                name = form.cleaned_data['name'],
                element = form.cleaned_data['element'],
                color = color,
                btn = btn,
                user = request.user
            )

            return redirect('profile')

    else :
       form = forms.DeviceCreationForm()


    return render(request , 'home/send_device.html' , { 'form' : form })

class DeviceListView(ListView):
    model = models.device
    context_object_name = 'devices'
    template_name = 'home/list_device.html'
    def get_queryset(self):
        queryset = models.device.objects.all().filter(user = self.request.user)
        return queryset
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        if models.device.objects.all().filter(user = self.request.user):
            context['device1'] = models.device.objects.all().filter(user = self.request.user)[0]
            context['device2'] = models.device.objects.all().filter(user = self.request.user)[1]
            context['lastData'] = models.GrafData.objects.all().filter(user = self.request.user).last()
            if context['lastData'].gas >= 100:
                gasStatus = True
            else:
                gasStatus = False
            context['gasStatus'] = gasStatus
            context['motion_detected'] = MotionDetectors.objects.all().filter(user = self.request.user).first()
            print(context["lastData"])
            pack = models.Package.objects.filter(user = self.request.user, enabled = True).first()
            if pack.name != "خالی":
                context['package_alert'] = True
            else:
                context['package_alert'] = False
        return context
 
    
def post_device(request):
    if request.method == 'GET':
        # Validation data
        form = forms.GUIOrderClassModelCreationForm(request.GET)
        if not form.is_valid() :
            device = models.device.objects.all().filter(device = form.cleaned_data['device'].device).first()
            home = models.Home.objects.all().filter(user = device.user).first()

            models.GUIOrderClassModel.objects.create(
                name = "Off by person order",
                type = 1,
                status = form.cleaned_data['status'],
                detail = {"message" : "Off by person order"},
                device = device,
                home = home,
                color = device.color,
                btn = device.btn,
                data = form.cleaned_data['data']
            )
                        
            models.device.objects.all().filter(device = form.cleaned_data['device'].device).update(status = form.cleaned_data['status'], data = form.cleaned_data["data"])
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
    motion_detected = MotionDetectors.objects.all().filter(user = request.user).first()    # check kardan queryset haye khane
    return render(request, 'account/profile.html', {"home": home, "user": user, "usage": usage, "e_total_usage": e_total_usage, "w_total_usage": w_total_usage, "g_total_usage": g_total_usage, "int_e" : int_e, "int_g" : int_g, "int_w" : int_w,"is_fire" : is_fire, "temp" : temp, "total_temp" : total_temp, "isEarthHum":isEarthHum, "hum": hum, "total_hum": total_hum, "motion" : motion, "total_gas" : gas, "gas" : gas, "cityStatus":cityStatus, "cityTemp":cityTemp, 'motion_detected' : motion_detected})


class CommentListView(ListView):
    model = models.Comment
    context_object_name = 'comments'
    template_name = 'home/faq.html'
    queryset = models.Comment.objects.all().order_by('-created').filter(status = True)

class listPackage(ListView):
    model = models.Package
    context_object_name = 'packs'
    template_name = 'home/listPacks.html'
    queryset = models.Package.objects.all().order_by('-id').filter(visible = True)
    
    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)           
        context['pack1'] = models.Package.objects.all().filter(user = self.request.user).order_by('id')[2]
        context['pack2'] = models.Package.objects.all().filter(user = self.request.user).order_by('id')[3]
        context['pack3'] = models.Package.objects.all().filter(user = self.request.user).order_by('id')[0]
        context['pack4'] = models.Package.objects.all().filter(user = self.request.user).order_by('id')[4]
        context['pack5'] = models.Package.objects.all().filter(user = self.request.user).order_by('id')[1]
        context['motion_detected'] = MotionDetectors.objects.all().filter(user = self.request.user).first()
        if models.GrafData.objects.all().filter(user = self.request.user).last().gas >= 100:
            gasStatus = True
        else:
            gasStatus = False
        context['gasStatus'] = gasStatus
        return context

def sendPackage(request):
    if request.method == 'GET':
        form = forms.PackagesCreationForm(request.GET)
        if form.is_valid() :
            pack = models.Package.objects.filter(name=form.cleaned_data['name'], user = request.user)
            pack.update(name = form.cleaned_data['name'], description = form.cleaned_data['description'], enabled = form.cleaned_data['enabled'], visible = form.cleaned_data['visible'])
            packStatus = form.cleaned_data['enabled']
            if packStatus == True:
                packs = models.Package.objects.filter(user = request.user)
                for pk in packs:
                    pk.enabled = False
                    pk.save()
            pack.update(name = form.cleaned_data['name'], description = form.cleaned_data['description'], enabled = form.cleaned_data['enabled'], visible = form.cleaned_data['visible'])
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
    motion_detected = MotionDetectors.objects.all().filter(user = request.user).first()
    # check kardan queryset haye khane
    return render(request, 'account/profile.html', {"home": home, "user": user, "usage": usage, "e_total_usage": e_total_usage, "w_total_usage": w_total_usage, "g_total_usage": g_total_usage, "int_e" : int_e, "int_g" : int_g, "int_w" : int_w,"is_fire" : is_fire, "temp" : temp, "total_temp" : total_temp, "isEarthHum":isEarthHum, "hum": hum, "total_hum": total_hum, "motion" : motion, "total_gas" : gas, "gas" : gas, "cityStatus":cityStatus, "cityTemp":cityTemp, 'motion_detected' : motion_detected})
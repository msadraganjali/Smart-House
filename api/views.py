import json
import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from datetime import timedelta
from datetime import datetime

from . import serializers
from . import models as apiModels
from home import models

def updateAccuWheather(request):
    lastApiRequest = apiModels.AccuWheather.objects.get(user = request.user.uuid)
    nowTime = datetime.now()
    if lastApiRequest.time + timedelta(minutes=2) > nowTime:
        return lastApiRequest
    elif lastApiRequest.time + timedelta(minutes=2) <= nowTime:
        try:
            accuWheader = requests.get("https://dataservice.accuweather.com/currentconditions/v1/208194?apikey=BAi9KZGpuijwO3pKNPAgqb39uR54YJfm&language=fa-ir")
            if accuWheader.status_code == 200:
                responseCity = accuWheader.json()
                cityStatus = responseCity[0]["WeatherText"]
                cityTemp = responseCity[0]["Temperature"]["Metric"]["Value"]
                lastApiRequest.temp = cityTemp
                lastApiRequest.status = cityStatus
                lastApiRequest.save()
                lastApiRequest = apiModels.AccuWheather.objects.get(user = request.user.uuid)
                return lastApiRequest
            else:
                return lastApiRequest
        except:
            return lastApiRequest

# klass gereftan khane besorat api
class getHome(generics.RetrieveAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeViewSetSerializer
    lookup_field = 'password'

# klass post kardan vasiat tavasot kontor be sorat api
class postStatusToHome(APIView):
    permission_classes = (IsAuthenticated,)

    # fahmidan fasl
    def print_season(self, date):
        month = date.month
        day = date.day
        winter = False
        spring = False
        summer = False
        fall = False
        if month == 12 or month <= 2:
            winter = True
            return "winter"
        elif month >= 3 and month <= 5:
            spring = True
            return "spring"
        elif month >= 6 and month <= 8:
            summer = True
            return "summer"
        else:
            fall = True
            return fall

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        # gereftan fild hay json
        uuid = body['uuid']
        is_end = body['is_end']
        is_end_forever = body['is_end_forever']
        is_end_start = body['is_end_start']
        is_end_end = body['is_end_end']
        is_accident = body['is_accident']
        usage = body['usage']
        temp = body['temp']
        isEarthHum = body['isEarthHum']
        hum = body['hum']
        motion = body['motion']
        gas = body['gas']

        
        is_end = bool(is_end)
        is_end_forever = bool(is_end_forever)
        is_end_start = bool(is_end_start)
        is_end_end = bool(is_end_end)
        is_accident = bool(is_accident)
        isEarthHum = bool(isEarthHum)
        usage = int(usage)
        temp = float(temp)
        hum = float(hum)
        motion = bool(motion)
        gas = int(gas)
        print(gas)
        # gereftan khane
        home = models.Home.objects.filter(uuid=uuid).first()
        # check kardan khane
        if not home:
            return Response({"[SYSTEM_ERROR] => error_meseage": "the uuid not found..."}, status=status.HTTP_400_BAD_REQUEST)
        # check kardan is_accident
        
        if is_accident:
            models.Order.objects.create(name="is_accident", type=2, detail={"meseage": "this meseage is a accident please help"}, forever=True, home=home)
        # check kardan is_end, is_end_forever, is_end_start, is_end_end
        if is_end and is_end_forever and not is_end_end and not is_end_start:
            models.Order.objects.create(name="shot down", type=2, detail={
                                        "meseage": "shot down"}, forever=True, home=home.user.nid)
        if is_end and is_end_end and is_end_start and not is_end_forever:
            models.Order.objects.create(name="shot down", type=2, detail={
                                        "meseage": "shot down"}, forever=False, start=is_end_start, end=is_end_end, home=home.user.nid)
        serializer = serializers.HomeViewSetSerializer(home, many=False)
        # moteghayer hay lazem baraye anjame ghezavat!
        today = datetime.today()
        score_change = 0
        usage_str = ""
        # ghesmate ghzavat
        if self.print_season(today) == "summer" or self.print_season(today) == "spring":
            if usage <= 300 and home.locate == "معمولی":
                usage_str = "good"
                score_change = 1
            elif usage <= 3000 and home.locate == "گرمایی۱":
                usage_str = "good"
                score_change = 1
            elif usage <= 2000 and home.locate == "گرمایی۲":
                usage_str = "good"
                score_change = 1
            elif usage <= 1000 and home.locate == "گرمایی۳":
                usage_str = "good"
                score_change = 1
            elif usage <= 400 and home.locate == "گرمایی۴":
                usage_str = "good"
                score_change = 1
            else:
                usage_str = "bad"
                score_change = -4
        elif (self.print_season(today) == "winter" or self.print_season(today) == "fall"):
            if usage <= 200:
                usage_str = "good"
                score_change = 1
            else:
                usage_str = "bad"
                score_change = -4

        # moteghayer hay lazem baray save kardan log
        last_score = home.score
        home.score = last_score + score_change
        home_score = home.score
        # save kardan log
        models.localLog.objects.create(name="usagecheck", user=request.user, detail={
                                       "usage": usage_str, "score": last_score + score_change}, usage=usage)
        models.GrafData.objects.create(e_usage=usage, user=request.user, is_fire =  is_accident, temp = temp, isEarthHum = isEarthHum, hum = hum, motion = motion, gas = gas)
        # check kardane emtiaz
        if home_score <= -20:
            # moteghayer hay lazem baray ferestadan dastore ghate bargh!
            start = datetime.now()
            end = start + timedelta(hours=2)
            models.Order.objects.create(name="High Consumption", type=0, detail={
                                        "meseage": "Your consumption has been exceeded and you have experienced a power outage. Your negative score is 0, but a disciplinary case has been recorded for you"}, start=start, end=end, home = home)
            home.score = 0
            last_total_score = home.total_score
            home.total_score = last_total_score + 1
        # save kardan taghirat
        home.save()
        return Response({"status" : "you are sending data successfuly"}, status=status.HTTP_200_OK)

# sakhtan khane be vasile ye api
class CreateHome(generics.CreateAPIView):
    queryset = models.Home.objects.all()
    serializer_class = serializers.HomeViewSetSerializer

class getPhysicsOrder(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    
    def updateDevicesOfPackage(self, timeId):
        # queryset = get_object_or_404(models.TimeOfDevice, id=timeId)
        queryset = models.TimeOfDevice.objects.get(id=timeId)
        deviceTime = queryset.time
        deviceTime2 = queryset.time2
        nowTime = datetime.now()
        nowTime = nowTime.time()
        
        if deviceTime < nowTime and deviceTime2 > nowTime:
           queryset.status = 1
           queryset.isPackMode = True
           queryset.save()
        else:
           queryset.status = 0
           queryset.isPackMode = True
           queryset.save()

    def get_serializer_class(self):
        pack = models.Package.objects.all().filter(user = self.request.user, enabled=True).first()
        if pack.name == "خالی":
            return serializers.deviceSerializer
        else:
            return serializers.physicsOrderSerializer

    def get_queryset(self):
        pack = models.Package.objects.all().filter(user = self.request.user, enabled=True).first()
        times = models.TimeOfDevice.objects.filter(user = self.request.user, package = pack.id)
        devices = models.device.objects.filter(user = self.request.user)
        if pack.name == "خالی":
            for time in times:
                time.isPackMode = True
                time.save()
            return devices
        else:
            for time in times:
                self.updateDevicesOfPackage(time.id)
            return times

    def post(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
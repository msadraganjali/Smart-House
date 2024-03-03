import uuid
from django.db import models
from django.utils import timezone
from account.models import User

# klass model jadval home ke hameye object haye home in vijegi haro daran.
class Home(models.Model):
    LOCAL_CHOICES= (
        ("معمولی", "معمولی"),
        ("گرمایی۱", "گرمایی۱"),
        ("گرمایی۲", "گرمایی۲"),
        ("گرمایی۳", "گرمایی۳"),
        ("گرمایی۴", "گرمایی۴"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True ,default = uuid.uuid4,)
    score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)
    locate = models.CharField(choices=LOCAL_CHOICES, max_length=10)
    password = models.CharField(max_length=255)
    pccode = models.CharField(max_length=10)
    electricity_number = models.CharField(max_length=14)
    gaz_number = models.CharField(max_length=14)
    whater_number = models.CharField(max_length=14)
    def __str__(self):
        return f"user_nid : {str(self.user.nid)},  pccode : {self.pccode}"

# dastorati ke ghara ast be kontor ha ersal beshan ke bekhater nadashtan teknoloji be samt database ersal mishan!
class Order(models.Model):
    TYPE_STOP = 0
    TYPE_START = 1
    TYPE_ALERT_DANGER = 2
    TYPE_LOG_CHICES = (
        (TYPE_STOP, 'توقف'),
        (TYPE_START, 'شروع'),
        (TYPE_ALERT_DANGER, 'خطر'),
    )
    name = models.CharField(max_length=255)
    type = models.SmallIntegerField(choices=TYPE_LOG_CHICES)
    date = models.DateTimeField(auto_now_add=True)
    detail = models.JSONField()
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    forever = models.BooleanField(default=False)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


# log hayi ke be dalile dashtan etelaat lazem dar database zskhire mishavand!
class localLog(models.Model):
    name = models.CharField(max_length=100000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    usage = models.CharField(max_length=10000000000)
    detail = models.JSONField()

    def __str__(self) -> str:
        return self.name    

# etelaati ke baraye nemodar dar database zskhire mishavand!
class GrafData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    e_usage = models.IntegerField()
    is_fire = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    temp = models.FloatField()
    isEarthHum = models.BooleanField() # 0 for True and 1 for False
    hum = models.FloatField()
    gas = models.IntegerField()
    motion = models.BooleanField()

    def __str__(self):
        return f"usage: {str(self.e_usage)}, date: {self.created}"

class device(models.Model):
    ELEMENT_CHICES = (
        ("آب", "آب"),
        ("برق", "برق"),
        ("گاز", "گاز"),
    )

    DEVICE_IS_OFF = 0
    DEVICE_IS_ON = 1
    DEVICE_STATUS_CHOICES = (
        (DEVICE_IS_ON, 'on'),
        (DEVICE_IS_OFF, 'off'),
    )

    name = models.CharField(max_length=255)
    device = models.IntegerField(primary_key=True)
    status = models.SmallIntegerField(choices = DEVICE_STATUS_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, default="blue")
    btn = models.CharField(max_length=10, default="blue")
    element = models.CharField(max_length=3, choices=ELEMENT_CHICES)
    password = models.CharField(max_length=50)
    data = models.IntegerField(null=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}+{self.name}"

class GUIOrderClassModel(models.Model):
    TYPE_STOP = 0
    TYPE_START = 1
    TYPE_ALERT_DANGER = 2
    TYPE_LOG_CHICES = (
        (TYPE_STOP, 'توقف'),
        (TYPE_START, 'شروع'),
        (TYPE_ALERT_DANGER, 'خطر'),
    )
    name = models.CharField(max_length=255)
    type = models.SmallIntegerField(choices=TYPE_LOG_CHICES)
    date = models.DateTimeField(auto_now_add=True)
    detail = models.JSONField()
    status = models.BooleanField(default=False)
    device = models.ForeignKey(device, on_delete=models.CASCADE)
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    color = models.CharField(max_length=10, default="blue")
    btn = models.CharField(max_length=10, default="blue")
    data = models.IntegerField(null=True)

class Comment(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):  
        return f"{self.user.username} = {self.user.uuid} = {self.name}"

class Package(models.Model):
    name = models.CharField(max_length=255)
    enabled = models.BooleanField()
    description = models.TextField()
    visible = models.BooleanField()
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'packs')
    devices = models.ManyToManyField(device, related_name="package")

    def __str__(self):
        return f"{self.user.username} + {self.name}"

class TimeOfDevice(models.Model):
    
    DEVICE_IS_OFF = 0
    DEVICE_IS_ON = 1
    DEVICE_STATUS_CHOICES = (
        (DEVICE_IS_ON, 'on'),
        (DEVICE_IS_OFF, 'off'),
    )
    
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    device = models.ForeignKey(device, on_delete=models.CASCADE)
    time = models.TimeField()
    time2 = models.TimeField()
    status = models.SmallIntegerField(choices = DEVICE_STATUS_CHOICES)
    isPackMode = models.BooleanField(default=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="timeOfDevice")
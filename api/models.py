from django.db import models
from account.models import User

class AccuWheather(models.Model):
    temp = models.FloatField()
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    status = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} + {self.status} + {self.temp}"

class MotionDetectors(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateField(auto_now_add=True)
    status = models.BooleanField()
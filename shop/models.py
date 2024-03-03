from django.db import models
from account.models import User

# models haye kala ha
class Object(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='images/obj/')
    thumbnail2 = models.ImageField(upload_to='images/obj/')
    color = models.CharField(max_length=100)
    size = models.CharField(max_length=255)
    mark = models.CharField(max_length=255)
    masraf = models.IntegerField()
    price = models.FloatField()
    category = models.CharField(max_length=255)
    offprice = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class cart_obj(models.Model):

    CART_OBJ_COLOR_CHOICES = (
        ("black", "black"),
        ("white", "white"),
        ("red", "red"),
        ("blue", "blue"),
        ("green", "green"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    obj = models.ManyToManyField(Object)
    color = models.CharField(max_length=10, choices=CART_OBJ_COLOR_CHOICES)
    count = models.IntegerField()

    def __str__(self):
        return self.user.username
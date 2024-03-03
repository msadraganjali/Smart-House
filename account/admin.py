from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# register kardan modele user baznevisi shode ye user
admin.site.register(User, UserAdmin)

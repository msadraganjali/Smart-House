from django.contrib import admin
from . import models
# ezafe kardan model ha be panel admin
admin.site.register(models.Object)
admin.site.register(models.cart_obj)
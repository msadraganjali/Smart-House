from django.contrib import admin
from . import models

# register kardan model ha dar panele admin
# admin.site.register(models.Home)
@admin.register(models.Home)
class HomeAdmin(admin.ModelAdmin):
    class Meta:
        model = models.Home
    readonly_fields = ('uuid',)
admin.site.register(models.localLog)
admin.site.register(models.Order)
admin.site.register(models.GrafData)
admin.site.register(models.device)
admin.site.register(models.GUIOrderClassModel)
admin.site.register(models.Comment)
admin.site.register(models.Package)
admin.site.register(models.TimeOfDevice)
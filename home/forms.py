from django import forms
from . import models

# klass formi sakhte khane.
class HomeCreationForm(forms.ModelForm):
    class Meta:
        model = models.Home
        fields = ["user", "locate", "password", "pccode", "electricity_number", "gaz_number", "whater_number"]

class DeviceCreationForm(forms.ModelForm):
    class Meta:
        model = models.device
        fields = ["user", "name", "element"]

class GUIOrderClassModelCreationForm(forms.ModelForm):
    class Meta:
        model = models.GUIOrderClassModel
        fields = ["name", "type", "detail", "status", "device", "home", "data"]

class PackagesCreationForm(forms.ModelForm):
    class Meta:
        model = models.Package
        fields = ["name", "enabled", "description", "visible"]
from django import forms
from . import models
# class form haye site
class CartAddObjsForm(forms.Form):
    class Meta:
        model = models.cart_obj
        fields = "__all__"
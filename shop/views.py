from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from . import models
from . import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView

# class list kardan kala ha
class ObjectListView(ListView):
    model = models.Object
    context_object_name = 'objects'
    template_name = 'objects/index.html'
    queryset = models.Object.objects.all().order_by('masraf')

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_new'] = models.Object.objects.all().order_by('-created', '-updated')
        context['objects'] = models.Object.objects.all().order_by('masraf')
        return context

# class joseiate kala ye
class ObjectDetailView(DetailView):
    model = models.Object
    context_object_name = 'object'
    template_name = 'objects/detail.html'

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddCartFormView(FormView):
    template_name = 'objects/send.html'
    form_class = forms.CartAddObjsForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.user = self.request.user.id
        form.instance.obj = models.Object.objects.all().filter(id=self.request.GET['obj']).first()
        form.save()
        return super().form_valid(form)
    def form_invalid(self, form):
        return HttpResponse(form.errors)
from . import views
from django.urls import path, include
# address haye apilication
app_name = 'shop'
urlpatterns = [
    path("", views.ObjectListView.as_view() , name="list"),
    path("<int:pk>/", views.ObjectDetailView.as_view() , name="detail"),
    path("send/", views.AddCartFormView.as_view() , name="send"),
]

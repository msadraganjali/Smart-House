from . import views
from rest_framework.routers import SimpleRouter
from django.urls import path, include
# address haye apilication api
urlpatterns = [
    path("get_home/<slug:password>", views.getHome.as_view()),
    path("post_status_to_home/", views.postStatusToHome.as_view()),
    path("create_home/", views.CreateHome.as_view()),
    path("get_physics_order/", views.getPhysicsOrder.as_view()),
]

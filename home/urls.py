from django.urls import path
from . import views
app_name = "home"
# address haye applicatione home
urlpatterns = [
    path("create_home/", views.CreateHomeView.as_view(), name="send"),
    path("create_device/", views.send, name="send_device"),
    path("post_device/", views.post_device, name="post_device"),
    # path("post_device/", views.GUIOrderClassModelView.as_view(), name="post_device"),
    path("list_device/", views.DeviceListView.as_view(), name="list_device"),
    path("", views.HomeView.as_view(), name="index"),
    path("guide/", views.GuideView.as_view(), name="guide"),
    path("about_me/", views.AboutMe.as_view(), name="about_me"),
    path("faq/", views.CommentListView.as_view() , name="faq"),
    path("listPacks/", views.listPackage.as_view() , name="listpacks"),
    path("sendPacks/", views.sendPackage , name="packs"),
]
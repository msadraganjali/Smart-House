from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import UserCreationForm

# moteghayere mahdod kardan dastresy karbar be forme login
user_guest = user_passes_test(lambda u: not u.is_authenticated, '/', None)
# address haye marbot be ehraze hoviat
urlpatterns = [
    path('login/', user_guest(views.LoginView.as_view()), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
]
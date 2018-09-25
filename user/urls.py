from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('pref/', views.get_preference, name='get_prefernce')
]

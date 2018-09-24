from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('preference/', views.get_preference, name='get_prefernce')
]

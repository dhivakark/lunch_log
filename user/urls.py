from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('preference/', views.get_preference, name='get_prefernce'),
    path('weekly_entry/', views.weekly_entry, name='weekly_entry'),
    path('weekly_entry/week_updated/', views.week_updated, name='week_updated'),
]

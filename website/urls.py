from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lottery/', views.lottery, name='lottery'),
    path('get_winner/', views.get_winner, name='get_winner'),
    path('reset_winners/', views.reset_winners, name='reset_winners'),

]

from django.urls import path
from . import views

urlpatterns = {
    path('', views.craw_data, name='index'),
}
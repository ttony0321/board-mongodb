from django.urls import path
from . import views

urlpatterns = {
    path('', views.index, name='index'),
    path('theqoo/', views.theqoo, name='theqoo'),
    path('humor/', views.humor, name='humor'),
    path('fmkorea/', views.fmkorea, name='fmkorea'),
    path('all_comm/', views.comments_index, name='all_comm'),
    path('all_view/', views.view_index, name='all_view'),

}

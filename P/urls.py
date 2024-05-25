
from django.contrib import admin
from django.urls import path
from P import views

urlpatterns = [

    path("", views.index, name='Home'),
    path("index/", views.home2, name='home2'),
    path("login", views.login_view, name='login'),
    path("getallvisitors", views.getallvisitors, name='getallvisitors'),
    path("allotseat", views.allotseat, name='allotseat'),
    path("addvehicle", views.addvehicle, name='addvehicle'),
    path("getallseatnum", views.getallseatnum, name='getallseatnum'),
    path("activevehicle", views.activevehicle, name='activevehicle'),
    path("exitvehicle", views.exitvehicle, name='exitvehicle'),
    path("addvisitor", views.addvisitor, name='addvisitor'),
    path("visitordetail", views.visitordetail, name='visitordetail'),
    path("parkschedule/", views.parkschedule, name='parkschedule'),
    path("logout",views.logout_us,name="logout"),
    path("visitor",views.visitor,name="visitor"),
    path("tracevehicle",views.tracevehicle,name="tracevehicle"),
    path('video_feed/', views.video_feed, name='video_feed'),
]

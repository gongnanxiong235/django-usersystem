from django.contrib import admin
from django.urls import path,include
from user import views

urlpatterns = [
    # path('login/',views.login),
    path('login/',views.Login.as_view()),
    path('index/',views.index),
    path('test/',views.test),
    path('regist/',views.Regist.as_view()),
]
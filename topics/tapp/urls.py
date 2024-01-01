"""
URL configuration for newsite1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from tapp import views
from django.urls import include
router = DefaultRouter()
router.register('tapp', views.TopicsViewSet, basename='tapp')

urlpatterns = [
    path("home", views.home, name = "home"),
    path("main", views.main, name = "main"),
    path("login", views.login, name = "login"),
    path("forget", views.forget, name = "forget"),
    path("signup", views.signup, name = "signup"),
    path("logout", views.logout, name = "logout"),
    path("change", views.change, name = "change"),
    path("health", views.health, name = "health"),
    path("world", views.world, name = "world"),
    path("environment", views.environment, name = "environment"),
    path("science", views.science, name = "science"),
    path("result", views.result, name = "result"),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) # API驗證URL
]
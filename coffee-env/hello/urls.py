from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name = "home"),
    path("start-coffee/", views.start_coffee, name="start_coffee")
]
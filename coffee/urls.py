from django.urls import path
from coffee import views

urlpatterns = [
    path("coffees", views.coffeeList.as_view(), name="user_coffees"),
    path("rate-roaster/", views.selectRoaster.as_view(), name="select_roaster"),
    path("rate-coffee/", views.selectCoffee.as_view(), name="select_coffee"),
    path("add-roaster/", views.roasterCreate.as_view(), name="add_roaster"),
    path("add-coffee/1", views.coffeeCreate1.as_view(), name="add_coffee1"),
    path("add-coffee/2", views.coffeeCreate2.as_view(), name="add_coffee2"),
    path("add-coffee/3", views.coffeeCreate3.as_view(), name="add_coffee3"),
    path("add-coffee/4", views.coffeeCreate4.as_view(), name="add_coffee4"),
]
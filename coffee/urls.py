from django.urls import path
from coffee import views

urlpatterns = [
    path("coffees", views.coffeeList.as_view(), name="user_coffees"),
    path("rate/1", views.selectRoaster.as_view(), name="select_roaster"),
    path("rate/2", views.selectCoffee.as_view(), name="select_coffee"),
    path("rate/3", views.selectBrew.as_view(), name="select_brew"),
    path("rate/4", views.selectRating.as_view(), name="select_rating"),
    path("<pk>/update", views.updateRating.as_view(), name="update_rating"),
    path("<pk>/delete", views.deleteRating.as_view(), name="delete_rating"),
    path("add-roaster/", views.roasterCreate.as_view(), name="add_roaster"),
    path("add-coffee/1", views.coffeeCreate1.as_view(), name="add_coffee1"),
    path("add-coffee/2", views.coffeeCreate2.as_view(), name="add_coffee2"),
    path("add-coffee/3", views.coffeeCreate3.as_view(), name="add_coffee3"),
    path("add-coffee/4", views.coffeeCreate4.as_view(), name="add_coffee4"),
]
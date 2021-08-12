from django.urls import path
from coffees import views

urlpatterns = [
    path("^user/(?P<username>[\w.@+-]+)/add-coffee/", views.add_coffee, name="add_coffee"),
    path("^user/(?P<username>[\w.@+-]+)/rate/", views.add_rating, name="add_rating")
]
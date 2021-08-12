from django.urls import path
from coffees import views

urlpatterns = [
    path('^user/(?P<username>[\w.@+-]+)/coffees/$', views.user_coffees, name='user_coffees'),
    path("^user/(?P<username>[\w.@+-]+)/add-coffee/", views.add_coffee, name="add_coffee")
]
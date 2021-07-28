from django.urls import path
from hello import views

urlpatterns = [
    path("", views.home, name = "home"),
    path('^user/(?P<username>[\w.@+-]+)/$', views.user_home, name='user_home'),
    path('^user/(?P<username>[\w.@+-]+)/profile/$', views.user_profile, name='user_profile'),
    path("^user/(?P<username>[\w.@+-]+)/add-coffee/", views.add_coffee, name="add_coffee")
]
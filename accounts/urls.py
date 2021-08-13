from django.urls import path,  url
from accounts import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # # url(r'^user/(?P<username>[\w.@+-]+)/$', views.user_home, name='user_home'),
    # url(r'^coffees/$', views.user_coffees, name='user_coffees'),
    # url(r'^profile/$', views.user_profile, name='user_profile'),
]
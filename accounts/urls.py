from django.urls import path
from accounts import views

urlpatterns = [
    path('^$', views.home, name='home'),
    path('^signup/$', views.signup, name='signup'),
    path('^user/(?P<username>[\w.@+-]+)/$', views.user_home, name='user_home'),
    path('^user/(?P<username>[\w.@+-]+)/profile/$', views.user_profile, name='user_profile'),
]
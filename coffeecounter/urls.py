"""coffeecounter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from coffees import views

urlpatterns = [
    url(r'^$', accounts_views.home, name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', accounts_views.user_home, name='user_home'),
    url(r'^user/(?P<username>[\w.@+-]+)/coffees/$', views.user_coffees, name='user_coffees'),
    url(r'^user/(?P<username>[\w.@+-]+)/profile/$', accounts_views.user_profile, name='user_profile'),
    url(r'^user/(?P<username>[\w.@+-]+)/add-coffee/$', views.add_coffee, name="add_coffee"),
    url(r'^admin/', admin.site.urls),
]
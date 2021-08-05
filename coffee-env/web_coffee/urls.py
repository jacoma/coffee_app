"""web_coffee URL Configuration

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

from hello import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^user/(?P<username>[\w.@+-]+)/$', views.user_home, name='user_home'),
    url(r'^user/(?P<username>[\w.@+-]+)/profile/$', views.user_profile, name='user_profile'),
    url(r'^user/(?P<username>[\w.@+-]+)/add-coffee/$', views.add_coffee, name="add_coffee"),
    url(r'^admin/', admin.site.urls),
]

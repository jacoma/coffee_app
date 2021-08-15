from django.urls import path
from coffee import views
from coffee.views import FORMS

urlpatterns = [
    # path("add-coffee/", views.add_coffee, name="add_coffee"),
    path("rate/", views.RatingWizard.as_view(FORMS), name="rate_coffee"),
    # path('^coffees/$', views.user_coffees, name='user_coffees'),
    # url(r'^user/(?P<username>[\w.@+-]+)/$', accounts_views.user_home, name='user_home'),
]
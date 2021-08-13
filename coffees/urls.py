from django.urls import path
from coffees import views

urlpatterns = [
    path("^add-coffee/", views.add_coffee, name="add_coffee"),
    path("^rate/", views.RatingWizard.as_view(), name="rate_coffee")
]
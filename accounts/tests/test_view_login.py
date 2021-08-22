from django.urls import reverse, resolve
from django.test import TestCase
from accounts import views as accounts_views
from django.contrib.auth.models import User

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, accounts_views.home)
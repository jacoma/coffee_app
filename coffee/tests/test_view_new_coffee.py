from django.urls import reverse, resolve
from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from ..forms import *
from coffee.views import *
from ..models import *

class RateCoffeeTests(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='Django', 
            password='1X<ISRUkw+tuK', 
            email = 'django@gmail.com')
        self.test_roaster = dim_roaster.objects.create(name='Test Roaster')
        self.country = countries.objects.create(
            country_code = 1,
            name = 'Test',
            country_code_alpha='te',
            country_code_alpha3	= 'tes',
            name_long= 'testing',      
            latitude= 24.55,
            longitude= 24.55)
        self.variety = dim_varietal.objects.create(varietal='testing')
        varietals_x=dim_varietal.objects.filter(varietal='test')
        self.notes = dim_notes.objects.create(flavor_notes = 'testing')
        notes_x=dim_notes.objects.filter(flavor_notes = 'testing')
        self.test_coffee = dim_coffee.objects.create(
            coffee_id = 1,
            name = 'test_coffee',
            roaster = self.test_roaster,
            farmer = 'test',
            country = self.country,
            process = 'washed',
            elevation = 1000
        )
        self.test_coffee.varietals.set(varietals_x)
        self.test_coffee.roaster_notes.set(notes_x)
        self.client.login(username='Django', password='1X<ISRUkw+tuK')
        self.url = reverse('select_roaster')

    def test_user_authentication(self):
        '''
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign up.
        '''
        response = self.client.get(self.url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

    def test_rate_coffee_view_success_status_code(self):
        url = self.url
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_csrf(self):
        url = self.url
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = self.url
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, roasterForm)

    def test_select_roaster_url_resolves_select_roaster_view(self):
        view = resolve('/rate/1')
        self.assertEquals(view.func.__name__, selectRoaster.as_view().__name__)

    def test_rate_coffee_valid_roaster_data(self):
        url = self.url
        data = {
            'name': 'Test Roaster'
        }
        response = self.client.post(url, data)
        self.assertEqual(self.client.session['roaster'], 'Test Roaster')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("select_coffee"))

    def test_select_roaster_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = self.url
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

### TEST SELECT COFFEE PAGE
    def test_select_coffee_contains_roaster(self):
        request_factory = RequestFactory().get('/')
        middleware = SessionMiddleware()
        middleware.process_request(request_factory)
        request_factory.session.save()
        request_factory.session['roaster']='Test Roaster'
        request_factory.session.save()
        view = selectCoffee()
        view.setup(request_factory)

        kwargs = view.get_form_kwargs()
        self.assertIn('roaster', kwargs)

        form = view.get_form(coffeeForm)
        self.assertInHTML('<option value="1">test_coffee</option>', str(form))

### TEST MODEL FORM?????

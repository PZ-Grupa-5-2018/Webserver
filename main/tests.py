from django.contrib.auth.models import User
from django.test import TestCase

from main.forms import LoginForm
from main.models import Monitor
from django.test import Client


class MonitorTestCase(TestCase):
    def setUp(self):
        Monitor.objects.create(name="Monitor I", url="https://pz-monitor.herokuapp.com/")
        Monitor.objects.create(name="Monitor II", url="https://pz-monitor-2.herokuapp.com")
        Monitor.objects.create(name="Monitor III", url="")

    def test_monitors_correct_url(self):
        monitor1 = Monitor.objects.get(name="Monitor I")
        monitor2 = Monitor.objects.get(name="Monitor II")
        self.assertEqual(str(monitor1), 'https://pz-monitor.herokuapp.com/')
        self.assertEqual(str(monitor2), 'https://pz-monitor-2.herokuapp.com/')


class LoginAndRegisterViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Pawel', last_name='Najuch', password='test12345', email='pawel.najch@test.com',
                            username='najuch')
        User.objects.create(username='admin', email='admin@admin.com', password='admin12345', is_staff=True)

    def test_login_page_get(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<small>Logowanie</small>', status_code=200)

    def test_login_page_form(self):
        cd = {'username': 'admin', 'password': 'admin12345'}
        form = LoginForm(data=cd)
        self.assertTrue(form.is_valid())

    def test_login_page_post(self):
        cd = {'username': 'admin', 'password': 'admin12345'}
        c = Client()
        response = c.post('/login/', cd)
        self.assertEqual(response.status_code, 200)

    def test_login_page_with_logged(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_measurementComplex_page_without_login(self):
        c = Client()
        response = c.get('/complexMeasurements/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/?next=/complexMeasurements/')

    def test_measurementComplex_page_logged(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get('/complexMeasurements/')
        self.assertEqual(response.status_code, 200)




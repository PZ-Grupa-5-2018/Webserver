from unittest import skip

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from main.forms import LoginForm, RegisterUserForm
from main.models import Monitor, validate_url, CustomMeasurement
from django.test import Client


class HomePageTestCase(TestCase):
    def test_home_page(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 200)


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

    def test_monitors_validate_url(self):
        self.assertRaises(ValidationError, validate_url, value="1234")


class LoginRegisterLogoutViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(first_name='Pawel', last_name='Najuch', password='test12345', email='pawel.najch@test.com',
                            username='najuch')
        User.objects.create(username='admin', email='admin@admin.com', password='admin12345', is_staff=True)

    def test_login_page_get(self):
        c = Client()
        response = c.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<small>Login</small>', status_code=200)

    def test_login_page_post_error(self):
        cd = {'username': 'admins', 'password': 'admin12345'}
        c = Client()
        response = c.post('/login/', cd)
        self.assertEqual(response.status_code, 200)

    def test_login_page_post_ok(self):
        cd = {'username': 'adminadmin', 'password': 'admin12345'}
        c = Client()
        user = User.objects.create_user(**cd)
        response = c.post('/login/', cd, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_page_with_logged(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get('/login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_register_page_without_login(self):
        c = Client()
        response = c.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_logged(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get('/register/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_register_post(self):
        c = Client()
        data = {'username': 'admin2', 'password': 'admin12345', 'password_confirm': 'admin12345',
                'first_name': 'admin2', 'last_name': 'admin2', 'email': 'admin2@admin2.com'}
        response = c.post('/register/', data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_register_post_with_error(self):
        c = Client()
        data = {'username': 'admin2'}
        response = c.post('/register/', data)
        self.assertEqual(response.status_code, 200)

    def test_logout_page_without_login(self):
        c = Client()
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=/logout/', target_status_code=200, fetch_redirect_response=True)
        response = c.get(response.url)
        self.assertEqual(response.status_code, 200)

    def test_logout_page_logged(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)


class LoginAndRegisterForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin', email='admin@admin.com', password='admin12345', is_staff=True)

    def test_login_page_form(self):
        cd = {'username': 'admin2', 'password': 'admin12345'}
        form = LoginForm(data=cd)
        self.assertTrue(form.is_valid())

    def test_register_form(self):
        data = {'username': 'adm', 'password': 'admi', 'password_confirm': 'adm5',
                'first_name': 'admin2', 'last_name': 'admin2', 'email': 'admin@admin.com'}
        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())

        data = {'username': 'admin3', 'password': 'admin12', 'password_confirm': 'admin13',
                'first_name': 'admin2', 'last_name': 'admin2', 'email': 'admin2@admin2.com'}
        form = RegisterUserForm(data=data)
        self.assertFalse(form.is_valid())


class ComplexMeasurements(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin', email='admin@admin.com', password='admin12345', is_staff=True)
        CustomMeasurement.objects.create(owner=User.objects.get(username="admin"), name="TEST", url="url", host_id=1,
                                         monitor_id=1, metric_id=1, period=1, created=timezone.now(),
                                         metric_type="mean")
        Monitor.objects.create(name="Monitor II", url="https://pz-monitor-2.herokuapp.com")

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

    def test_add_custom_measurement_page_view(self):
        c = Client()
        response = c.get("/monitors/1/hosts/1/add_custom_measurement_page/")
        self.assertEqual(response.status_code, 200)

    @skip("Don't want to test")
    def test_add_complex_measurement(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get("/monitors/1/hosts/1/add_custom_measurement_page/add_complex_measurement/",
                         {"custom_measurement_nam": "", "metric_type": "", "time_period": "", "type": "mean"})
        self.assertEqual(response.status_code, 200)

    @skip("Don't want to test")
    def test_ComplexMeasurementsDelete(self):
        c = Client()
        c.force_login(User.objects.get(username="admin"))
        response = c.get("/customDelete/1")
        self.assertEqual(response.status_code, 200)


class MonitorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='admin', email='admin@admin.com', password='admin12345', is_staff=True)
        Monitor.objects.create(name="Monitor II", url="https://pz-monitor-2.herokuapp.com")

    def test_getMonitorHosts(self):
        c = Client()
        response = c.get("/monitors/1/download_monitor_data/")
        self.assertEqual(response.status_code, 200)

    def test_downloadMonitorDetails(self):
        c = Client()
        response = c.get("/monitors/1/get_monitor_hosts/")
        self.assertEqual(response.status_code, 200)

    def test_getLastMeasurementsView(self):
        c = Client()
        response = c.get("/monitors/1/get_last_measurements")
        self.assertEqual(response.status_code, 200)

    def test_getLastMeasurementsFromMonitorListView(self):
        c = Client()
        response = c.get("/monitors/_1_/get_last_measurements_from_monitor_list/")
        self.assertEqual(response.status_code, 200)

    def test_monitors(self):
        c = Client()
        response = c.get("/monitors/")
        self.assertEqual(response.status_code, 200)

    def test_monitors_detail(self):
        c = Client()
        response = c.get("/monitors/1/")
        self.assertEqual(response.status_code, 200)

    def test_historical_measurements(self):
        pass

    def test_refreshChartMeasurments(self):
        c = Client()
        response = c.get("/monitors/1/hosts/1/refresh_chart_measurements/")
        self.assertEqual(response.status_code, 200)

    @skip("Don't want to test")
    def test_checkActiveSensors(self):
        c = Client()
        response = c.get("/monitors/1/check_active_sensors/")
        self.assertEqual(response.status_code, 200)

    def test_hosts_detail(self):
        c = Client()
        response = c.get("/monitors/1/hosts/1/")
        self.assertEqual(response.status_code, 200)

    def test_metrics_detail(self):
        c = Client()
        response = c.get("/monitors/1/hosts/1/metrics/1/")
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        c = Client()
        response = c.get("/search/")
        self.assertEqual(response.status_code, 200)

    def test_search_host(self):
        c = Client()
        response = c.get("/search/search_host/", {"search_generic": "", "search_type": "generic"})
        self.assertEqual(response.status_code, 200)
        response = c.get("/search/search_host/",
                         {"search_generic": "advanced", "search_type": "", "search_name": "", "search_ip": "",
                          "search_mac": "",
                          "CPU": "on", "RAM": "on", "HDD": "on"})
        self.assertEqual(response.status_code, 200)

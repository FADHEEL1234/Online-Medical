from django.test import TestCase, Client
from django.urls import reverse


class TestRegistration(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('user-register')

    def test_successful_registration(self):
        data = {
            'username': 'testuser',
            'email': 'a@b.com',
            'password': 'abcd1234',
            'password_confirm': 'abcd1234'
        }
        resp = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('message', resp.json())
        self.assertEqual(resp.json()['message'], 'User registered successfully')

    def test_password_mismatch(self):
        data = {
            'username': 'testuser2',
            'email': 'b@c.com',
            'password': 'abcd1234',
            'password_confirm': 'different'
        }
        resp = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Passwords do not match', resp.content.decode())


class TestToken(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user-register')
        self.token_url = reverse('token_obtain_pair')
        # create a user so token endpoint can be tested
        self.client.post(self.register_url, {
            'username': 'tokentest',
            'email': 't@t.com',
            'password': 'abcd1234',
            'password_confirm': 'abcd1234'
        }, content_type='application/json')

    def test_token_response_includes_username(self):
        resp = self.client.post(self.token_url, {
            'username': 'tokentest',
            'password': 'abcd1234'
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('access', data)
        self.assertIn('refresh', data)
        # custom field
        self.assertIn('username', data)
        self.assertEqual(data['username'], 'tokentest')
        # by default new user is not staff
        self.assertIn('is_staff', data)
        self.assertFalse(data['is_staff'])

    def test_staff_flag_in_token_for_admin_users(self):
        # create an admin user and verify the flag is True
        from django.contrib.auth.models import User
        admin = User.objects.create_superuser('adminuser', 'adm@in.com', 'password123')
        resp = self.client.post(self.token_url, {
            'username': 'adminuser',
            'password': 'password123'
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get('is_staff'))
        self.assertTrue(data.get('is_superuser'))


class TestAdminEndpoints(TestCase):
    def setUp(self):
        from django.contrib.auth.models import User
        self.client = Client()
        # normal user
        self.user = User.objects.create_user('normal', 'n@o.com', 'pass1234')
        # staff user
        self.staff = User.objects.create_user('staff', 's@t.com', 'pass1234', is_staff=True)
        # URLs
        self.doctor_create_url = reverse('doctor-create')
        self.doctor_list_url = reverse('doctor-list')

        # authenticate helper
    
    def authenticate(self, user):
        # obtain token and set header
        resp = self.client.post(reverse('token_obtain_pair'), {
            'username': user.username,
            'password': 'pass1234'
        }, content_type='application/json')
        token = resp.json().get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'

    def test_nonstaff_cannot_create_doctor(self):
        self.authenticate(self.user)
        resp = self.client.post(self.doctor_create_url, {
            'name': 'Test Dr',
            'specialization': 'Cardiology',
            'email': 'dr@test.com',
            'phone': '12345',
            'available_from': '08:00',
            'available_to': '16:00',
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 403)

    def test_staff_can_create_and_list_doctors(self):
        self.authenticate(self.staff)
        resp = self.client.post(self.doctor_create_url, {
            'name': 'Staff Dr',
            'specialization': 'Pediatrics',
            'email': 'staffdr@test.com',
            'phone': '67890',
            'available_from': '08:00',
            'available_to': '16:00',
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        # the availability fields should be reflected
        self.assertEqual(data['available_from'], '08:00:00')
        self.assertEqual(data['available_to'], '16:00:00')
        # ensure doctor appears in list
        resp2 = self.client.get(self.doctor_list_url)
        self.assertEqual(resp2.status_code, 200)
        self.assertTrue(any(d['name'] == 'Staff Dr' for d in resp2.json()))

    def test_staff_can_update_doctor_availability(self):
        self.authenticate(self.staff)
        # create doctor first
        resp = self.client.post(self.doctor_create_url, {
            'name': 'Update Dr',
            'specialization': 'General',
            'email': 'updatedr@test.com',
            'phone': '00000',
            'available_from': '09:00',
            'available_to': '17:00',
        }, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        doc_id = resp.json()['id']
        # now patch availability
        patch_resp = self.client.patch(reverse('doctor-detail', args=[doc_id]), {
            'available_from': '10:00',
            'available_to': '18:00'
        }, content_type='application/json')
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()['available_from'], '10:00:00')
        self.assertEqual(patch_resp.json()['available_to'], '18:00:00')

    def test_user_cannot_book_outside_availability(self):
        # create a doctor with narrow availability
        from appointments.models import Doctor
        doctor = Doctor.objects.create(
            name='Busy Dr', specialization='Busy', email='busy@h.com', phone='111',
            available_from='09:00', available_to='10:00'
        )
        # register and login client
        self.client.post(reverse('user-register'), {
            'username': 'patient', 'email': 'p@p.com',
            'password': 'testpass', 'password_confirm': 'testpass'
        }, content_type='application/json')
        resp = self.client.post(reverse('token_obtain_pair'), {
            'username': 'patient', 'password': 'testpass'
        }, content_type='application/json')
        token = resp.json().get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        # attempt to book at 11am
        from django.utils import timezone
        from datetime import timedelta
        future = timezone.now() + timedelta(days=1)
        bad_time = future.replace(hour=11, minute=0, second=0, microsecond=0)
        appt_resp = self.client.post(reverse('appointment-list-create'), {
            'doctor': doctor.id,
            'appointment_date': bad_time.isoformat()
        }, content_type='application/json')
        self.assertEqual(appt_resp.status_code, 400)
        self.assertIn('after the doctor', appt_resp.content.decode())

    def test_staff_can_change_appointment_status(self):
        # create an appointment as a normal user
        from appointments.models import Doctor, Appointment
        # make a doctor available anytime
        doctor = Doctor.objects.create(
            name='Dr Status', specialization='Test', email='status@h.com', phone='222',
            available_from='00:00', available_to='23:59'
        )
        # register patient
        self.client.post(reverse('user-register'), {
            'username': 'patient2', 'email': 'p2@p.com',
            'password': 'testpass', 'password_confirm': 'testpass'
        }, content_type='application/json')
        resp = self.client.post(reverse('token_obtain_pair'), {
            'username': 'patient2', 'password': 'testpass'
        }, content_type='application/json')
        token = resp.json().get('access')
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {token}'
        from django.utils import timezone
        from datetime import timedelta
        when = timezone.now() + timedelta(days=1)
        appt_resp = self.client.post(reverse('appointment-list-create'), {
            'doctor': doctor.id,
            'appointment_date': when.isoformat()
        }, content_type='application/json')
        # should succeed; if not, include response body to help debug
        self.assertEqual(appt_resp.status_code, 201, appt_resp.content.decode())
        data = appt_resp.json()
        self.assertIn('id', data, f"appointment creation returned {data}")
        appt_id = data['id']
        # now switch to staff and patch status
        self.authenticate(self.staff)
        patch = self.client.patch(reverse('admin-appointment-detail', args=[appt_id]),
                                   {'status': 'Approved'}, content_type='application/json')
        self.assertEqual(patch.status_code, 200)
        self.assertEqual(patch.json()['status'], 'Approved')


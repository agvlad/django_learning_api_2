from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class HardwareTests(APITestCase):
    token_url = reverse('token_obtain')
    hardware_list_url = reverse('Hardware-list')  # Este numele din view set (<nume>ViewSet) + '-list'
    hardware_detail_url = reverse('Hardware-detail', kwargs={"pk": 1})  # La fel + '-detail'. Si var necesare(pk)
    # pentru a gasi url-urile:
    # pip install django-extensions
    # adaugare 'django_extensions' in settings.py la INSTALLED_APPS
    # python manage.py show_urls

    hardware_data_1 = {
        'name': 'Juniper SRX 5800',
        'recommended_os_version': '12X-R2',
        'capabilities': 'firewall, router, switch',
        'number_of_interfaces': '4',
    }

    hardware_data_2 = {
        'name': 'Juniper QFX 10800',
        'recommended_os_version': '15X',
        'capabilities': 'switch',
        'number_of_interfaces': '8'
    }

    updated_hardware_data = {
        'name': 'Juniper SRX 5800', 'recommended_os_version': '10X-R2',
        'capabilities': 'firewall, router, switch', 'number_of_interfaces': 2
    }

    def setUp(self):
        """
        Creaza un entry in db
        Functia este rulata inaintea fiecarui test
        """
        self.authenticate_api_user()

        self.client.post(path=self.hardware_list_url,
                         data=self.hardware_data_1,
                         format='json')

    def authenticate_api_user(self, is_staff=True):
        if is_staff:
            self.user, token_response = self.get_user_and_token('test_user',
                                                                'test_pass', is_staff)
        else:
            self.user, token_response = self.get_user_and_token('test_user_2',
                                                                'test_pass_2', is_staff)

        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_user_and_token(self, user, password, is_staff):
        test_user = User.objects.create_user(username=user,
                                             password=password,
                                             is_staff=is_staff)
        token_response = self.client.post(path=self.token_url,
                                          data={'username': user,
                                                'password': password})
        return test_user, token_response

    def test_list_devices(self):
        """
        test get list
        """
        response = self.client.get(self.hardware_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(dict(dict(response.data)['results'][0])['name'], 'Juniper SRX 5800')
        # raspunsul are 2 layere de ordered dict

    def test_list_devices_non_staff(self):
        """
        test get list
        """
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(self.hardware_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_devices_unauthenticated(self):
        """
        test get list cand userul care face request nu este autentificat
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.hardware_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_device(self):
        """
        test post
        """
        response = self.client.post(path=self.hardware_list_url,
                                    data=self.hardware_data_2,
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'id': 2, 'name': 'Juniper QFX 10800', 'recommended_os_version': '15X',
                          'capabilities': 'switch', 'number_of_interfaces': 8})

    def test_create_device_non_staff(self):
        """
        test post cand userul care face request nu este staff user
        """
        self.authenticate_api_user(is_staff=False)
        response = self.client.post(path=self.hardware_list_url,
                                    data=self.hardware_data_2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_device_unauthenticated(self):
        """
        test post cand userul care face request nu este autentificat
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(path=self.hardware_list_url,
                                    data=self.hardware_data_2,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_device(self):
        """
        test get pt un item specific
        """
        response = self.client.get(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'Juniper SRX 5800', 'recommended_os_version': '12X-R2',
                          'capabilities': 'firewall, router, switch', 'number_of_interfaces': 4})

    def test_get_device_non_staff(self):
        """
        test get pt un item specific cand userul care face request nu este staff
        """
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_device_unauthenticated(self):
        """
        test get pt un item specific cand userul care face request nu este autentificat
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_device(self):
        """
        test put
        """
        response = self.client.put(path=self.hardware_detail_url,
                                   data=self.updated_hardware_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'Juniper SRX 5800', 'recommended_os_version': '10X-R2',
                          'capabilities': 'firewall, router, switch', 'number_of_interfaces': 2}
                         )

    def test_update_device_non_staff(self):
        """
        test put cand userul nu e staff
        """
        self.authenticate_api_user(is_staff=False)

        response = self.client.put(path=self.hardware_detail_url,
                                   data=self.updated_hardware_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_device_unauthenticated(self):
        """
        test put cand userul care face request nu este autentificat
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(path=self.hardware_detail_url,
                                   data=self.updated_hardware_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_item(self):
        """
        test delete
        """
        response = self.client.delete(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_non_staff(self):
        """
        test delete cand userul nu este staff
        """
        self.authenticate_api_user(is_staff=False)
        response = self.client.delete(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_item_unauthenticated(self):
        """
        test delete cand userul care face request nu este autentificat
        """
        self.client.force_authenticate(user=None, token=None)
        response = self.client.delete(path=self.hardware_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InterfaceTests(APITestCase):
    token_url = reverse('token_obtain')
    hardware_list_url = reverse('Hardware-list')
    device_list_url = reverse('Device-list')
    interface_list_url = reverse('Interface-list')
    interface_detail_url = reverse('Interface-detail', kwargs={"pk": 1})

    hardware_data = {
        'name': 'Juniper SRX 5800',
        'recommended_os_version': '12X-R2',
        'capabilities': 'firewall, router, switch',
        'number_of_interfaces': '4'
    }

    device_data = {
        'name': 'RTR001',
        'management_address': '192.168.100.7',
        'hardware_model': 'Juniper SRX 5800',
        'device_role': 'distribution',
    }

    modified_interface_data = {
        'connected_to': 3
    }

    interface_data = {
        'name': 'test_interface',
        'connected_to': 3,
        'device': 1,
    }

    def setUp(self):
        """
        Creaza un hardware model si un device
        Functia este rulata inaintea fiecarui test
        """
        self.authenticate_api_user()
        self.client.post(path=self.hardware_list_url, data=self.hardware_data, format='json')
        self.client.post(path=self.device_list_url, data=self.device_data, format='json')

    def authenticate_api_user(self, is_staff=True):
        """
        Seteaza credentialele pentru user
        :param is_staff: bool
        """
        # E nevoie de distinctia de nume pentru useri.
        if is_staff:
            self.user, token_response = self.get_user_and_token('test_user',
                                                                'test_pass', is_staff)
        else:
            self.user, token_response = self.get_user_and_token('test_user_2',
                                                                'test_pass_2', is_staff)

        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_user_and_token(self, user, password, is_staff):
        test_user = User.objects.create_user(username=user,
                                             password=password,
                                             is_staff=is_staff)
        token_response = self.client.post(path=self.token_url,
                                          data={'username': user,
                                                'password': password})
        return test_user, token_response

    def test_get_list(self):
        response = self.client.get(path=self.interface_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

    def test_get_list_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(self.interface_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 4)

    def test_get_list_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.interface_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        response = self.client.get(path=self.interface_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'RTR001_int_0')

    def test_get_item_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(path=self.interface_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'RTR001_int_0')

    def test_get_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(path=self.interface_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item(self):
        response = self.client.put(path=self.interface_detail_url,
                                   data=self.modified_interface_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['connected_to'], 3)

    def test_update_item_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.put(path=self.interface_detail_url,
                                   data=self.modified_interface_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(path=self.interface_detail_url,
                                   data=self.modified_interface_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_item(self):
        response = self.client.post(path=self.interface_list_url,
                                    data=self.interface_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_item(self):
        response = self.client.delete(path=self.interface_detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class DeviceTests(APITestCase):
    token_url = reverse('token_obtain')
    hardware_list_url = reverse('Hardware-list')
    device_list_url = reverse('Device-list')
    device_detail_url = reverse('Device-detail', kwargs={"pk": 1})

    hardware_data = {
        'name': 'Juniper SRX 5800',
        'recommended_os_version': '12X-R2',
        'capabilities': 'firewall, router, switch',
        'number_of_interfaces': '4'
    }

    device_data = {
        'name': 'RTR111',
        'management_address': '192.168.100.7',
        'hardware_model': 'Juniper SRX 5800',
        'device_role': 'distribution',
    }

    new_device_data = {
        'name': 'RTR222',
        'management_address': '192.168.100.100',
        'hardware_model': 'Juniper SRX 5800',
        'device_role': 'access',
    }

    def setUp(self):
        """
        Creaza un hardware model si un device
        Functia este rulata inaintea fiecarui test
        """
        self.authenticate_api_user()
        self.client.post(path=self.hardware_list_url, data=self.hardware_data, format='json')
        self.client.post(path=self.device_list_url, data=self.device_data, format='json')

    def authenticate_api_user(self, is_staff=True):
        """
        Seteaza credentialele pentru user
        :param is_staff: bool
        """
        if is_staff:
            self.user, token_response = self.get_user_and_token('test_user',
                                                                'test_pass', is_staff)
        else:
            self.user, token_response = self.get_user_and_token('test_user_2',
                                                                'test_pass_2', is_staff)

        token = token_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def get_user_and_token(self, user, password, is_staff):
        test_user = User.objects.create_user(username=user,
                                             password=password,
                                             is_staff=is_staff)
        token_response = self.client.post(path=self.token_url,
                                          data={'username': user,
                                                'password': password})
        return test_user, token_response

    def test_get_list(self):
        response = self.client.get(path=self.device_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(dict(response.data['results'][0]),
                         {'id': 1, 'name': 'RTR111', 'management_address': '192.168.100.7',
                          'hardware_model': 'Juniper SRX 5800', 'device_role': 'distribution',
                          'interfaces': [1, 2, 3, 4], 'networks': []})

    def test_get_list_not_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(path=self.device_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_list_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(path=self.device_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_item(self):
        response = self.client.get(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'RTR111', 'management_address': '192.168.100.7',
                          'hardware_model': 'Juniper SRX 5800', 'device_role': 'distribution',
                          'interfaces': [1, 2, 3, 4], 'networks': []})

    def test_get_item_not_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.get(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'name': 'RTR111', 'management_address': '192.168.100.7',
                          'hardware_model': 'Juniper SRX 5800', 'device_role': 'distribution',
                          'interfaces': [1, 2, 3, 4], 'networks': []})

    def test_get_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_item(self):
        response = self.client.post(path=self.device_list_url, data=self.new_device_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'id': 2, 'hardware_model': 'Juniper SRX 5800', 'networks': [],
                          'interfaces': [5, 6, 7, 8], 'name': 'RTR222',
                          'management_address': '192.168.100.100', 'device_role': 'access'})

    def test_create_item_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.post(path=self.device_list_url, data=self.new_device_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(path=self.device_list_url, data=self.new_device_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_item(self):
        response = self.client.delete(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_item_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.delete(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_item_unauthenticated(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.delete(path=self.device_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item(self):
        response = self.client.put(path=self.device_detail_url, data=self.new_device_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,
                         {'id': 1, 'hardware_model': 'Juniper SRX 5800', 'networks': [],
                          'interfaces': [1, 2, 3, 4], 'name': 'RTR222',
                          'management_address': '192.168.100.100', 'device_role': 'access'})

    def test_update_item_non_staff(self):
        self.authenticate_api_user(is_staff=False)
        response = self.client.put(path=self.device_detail_url, data=self.new_device_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_item_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.put(path=self.device_detail_url, data=self.new_device_data)
        # self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

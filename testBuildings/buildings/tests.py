import json
from django.test import TestCase
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Building, Floor


class BuildingPageListTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_buildings_url_allow_POST_GET(self):
        response = self.client.head(reverse('building_rest_list'))
        self.assertEqual(response['allow'], 'GET, POST, HEAD, OPTIONS')

    def test_GET_visitor_return_error(self):
        response = self.client.get(reverse('building_rest_list'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_GET_user_sees_only_his_buildings(self):
        user = self.log_user()
        response = self.client.get(reverse('building_rest_list'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['name'], 'b1')
        self.assertEqual(len(data), user.building_set.count())

    def test_GET_admin_sees_everything(self):
        self.client.login(username='myuser', password='password')
        response = self.client.get(reverse('building_rest_list'))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), Building.objects.count())

    def test_POST_visitor_return_error(self):
        response = self.client.post(reverse('building_rest_list'), data={
            'name': 'Building',
            'country': 'gr'
        })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_POST_user_insert_building(self):
        user = self.log_user()
        response = self.client.post(reverse('building_rest_list'), data={
            'name': 'Building',
            'country': 'gr'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Building')
        self.assertEqual(Building.objects.count(), 3)
        self.assertEqual(user.building_set.count(), 2)

    def test_POST_user_insert_building_error_name_country(self):
        user = self.log_user()
        response = self.client.post(reverse('building_rest_list'), data={})
        self.assertEqual(response.data['name'][0], 'This field is required.')
        self.assertEqual(response.data['country'][0], 'This field is required.')
        self.assertEqual(Building.objects.count(), 2)

class BuildingDetailViewTest(TestCase):
    def setUp(self):
        link = 'building_rest_detail'
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        user_b = User.objects.create_user(username='user_b', password='pass')
        b2 = Building.objects.create(user=user_b, name='b2', country='gr')

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_buildings_url_allow_GET_PUT_DELETE(self):
        response = self.client.head(reverse('building_rest_detail', kwargs={"pk": Building.objects.first().pk}))
        self.assertEqual(response['allow'], 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')

    def test_GET_visitor_return_error(self):
        response = self.client.get(reverse('building_rest_detail', kwargs={"pk": Building.objects.first().pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_GET_user_see_his_building(self):
        b1 = self.log_user().building_set.first()
        response = self.client.get(reverse('building_rest_detail', kwargs={"pk": b1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'b1')

    def test_GET_user_doesnt_see_other_buildings(self):
        self.log_user()
        b2 = Building.objects.filter(name='b2')[0]
        response = self.client.get(reverse('building_rest_detail', kwargs={"pk": b2.pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Permission denied.')

    def test_GET_user_not_found_building(self):
        self.log_user()
        response = self.client.get(reverse('building_rest_detail', kwargs={"pk": 0}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'], 'Not found.')

    def test_GET_admin_sees_everything(self):
        self.client.login(username='myuser', password='password')
        b1 = Building.objects.filter(name='b1')[0]
        response = self.client.get(reverse('building_rest_detail', kwargs={"pk": b1.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'b1')

class FloorPageListTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        b1_1 = Building.objects.create(user=user, name='b1_1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        floor1_1 = Floor.objects.create(building=b1_1, name="1_1 Floor", number=1, blueprint= abs_path)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="Second Floor", number=1, blueprint= abs_path)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_floor_url_allow_POST_GET(self):
        response = self.client.head(reverse('building_rest_list'))
        self.assertEqual(response['allow'], 'GET, POST, HEAD, OPTIONS')

    def test_GET_visitor_return_error(self):
        response = self.client.get(reverse('floor_rest_list', kwargs={"pk_building": Building.objects.first().pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_GET_user_see_floors_only_from_buildings(self):
        user = self.log_user()
        building = user.building_set.filter(name="b1")[0]
        response = self.client.get(reverse('floor_rest_list', kwargs={"pk_building": building.pk}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['name'], 'First Floor')
        self.assertEqual(len(data), building.floor_set.count())

    def test_GET_user_cannot_see_other_user_floors(self):
        user = self.log_user()
        response = self.client.get(reverse('floor_rest_list', kwargs={"pk_building": Building.objects.filter(name="b2")[0].pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Permission denied.')

    def test_GET_admin_see_floors_only_from_the_buildings(self):
        self.client.login(username='myuser', password='password')
        user = User.objects.get(username='me')
        building = user.building_set.filter(name="b1")[0]
        response = self.client.get(reverse('floor_rest_list', kwargs={"pk_building": building.pk}))
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]['name'], 'First Floor')
        self.assertEqual(len(data), building.floor_set.count())

    def test_POST_visitor_return_error(self):
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_rest_list', kwargs={"pk_building": Building.objects.first().pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp
            })
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_POST_user_insert_floor_for_building(self):
        building = self.log_user().building_set.first()
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_rest_list', kwargs={"pk_building": building.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp,
                'building': building.pk
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(building.floor_set.count(), 2)

    def test_POST_admin_insert_floor_for_other_users_building(self):
        self.client.login(username='myuser', password='password')
        user = User.objects.get(username='me')
        building =user.building_set.first()
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_rest_list', kwargs={"pk_building": building.pk}), data={
                'name': 'Floor',
                'number': 1,
                'blueprint': fp,
                'building': building.pk
            })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(building.floor_set.count(), 2)

    def test_POST_user_insert_floor_with_error(self):
        building = self.log_user().building_set.first()
        abs_path = finders.find('img/blueprint.jpg')
        with open(abs_path) as fp:
            response = self.client.post(reverse('floor_rest_list', kwargs={"pk_building": building.pk}), data={
                'name': 'Floor',
                'number': 1,
                'building': building.pk
            })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['blueprint'], 'No file was submitted.')

class FloorDetailViewTest(TestCase):
    def setUp(self):
        my_admin = User.objects.create_superuser('myuser', 'myemail@test.com', 'password')
        abs_path = finders.find('img/blueprint.jpg')
        user = User.objects.create_user(username='me', password='pass')
        b1 = Building.objects.create(user=user, name='b1', country='gr')
        b1_1 = Building.objects.create(user=user, name='b1_1', country='gr')
        floor1 = Floor.objects.create(building=b1, name="First Floor", number=1, blueprint= abs_path)
        floor1_1 = Floor.objects.create(building=b1_1, name="1_1 Floor", number=1, blueprint= abs_path)
        user2 = User.objects.create_user(username='me2', password='pass')
        b2 = Building.objects.create(user=user2, name='b2', country='gr')
        floor2 = Floor.objects.create(building=b2, name="Second Floor", number=1, blueprint= abs_path)

    def log_user(self):
        user = User.objects.get(username='me')
        self.client.login(username=user.username, password='pass')
        return user

    def test_floor_url_allow_GET_PUT_DELETE(self):
        building = Building.objects.filter(name="b1")[0]
        response = self.client.head(reverse('floor_rest_detail', kwargs={"pk_building": building.pk, "pk": building.floor_set.first().pk}))
        self.assertEqual(response['allow'], 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS')

    def test_GET_visitor_return_error(self):
        building = Building.objects.filter(name="b1")[0]
        response = self.client.get(reverse('floor_rest_detail',  kwargs={"pk_building": building.pk, "pk": building.floor_set.first().pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')

    def test_GET_user_see_his_floor(self):
        b1 = self.log_user().building_set.first()
        response = self.client.get(reverse('floor_rest_detail',  kwargs={"pk_building": b1.pk, "pk": b1.floor_set.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], '1_1 Floor')

    def test_GET_user_cant_see_floor_of_other_user_building(self):
        self.log_user()
        b2 = Building.objects.filter(name='b2')[0]
        response = self.client.get(reverse('floor_rest_detail',  kwargs={"pk_building": b2.pk, "pk": b2.floor_set.first().pk}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data['detail'], 'Permission denied.')

    def test_GET_admin_can_see_everything(self):
        self.client.login(username='myuser', password='password')
        b1 = Building.objects.filter(name='b1')[0]
        response = self.client.get(reverse('floor_rest_detail',  kwargs={"pk_building": b1.pk, "pk": b1.floor_set.first().pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'First Floor')

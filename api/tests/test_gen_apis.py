from api.models import Staff
from django.contrib.auth.models import Permission, Group
from rest_framework.test import APITestCase
from django.urls import reverse



class GenreTest(APITestCase):
    def setUp(self):
        self.login = reverse("token_obtain_pair")
        self.list_create_genre = reverse("list_create_genre")

        admin = Staff.objects.create_user(
            username="Thimmy",
            password = "1234qwer",
            is_staff = True,
            is_active = True,
            is_superuser = True
        )
        
        view_genre_staff = Staff.objects.create_user(
            username="Thommy",
            password = "1234qwer",
            is_staff = True,
            is_active = True
        )

        add_genre_staff = Staff.objects.create_user(
            username="Thiwo",
            password = "1234qwer",
            is_staff = True,
            is_active = True
        )

        '''
            Create a grp for view_genre
            Get the view_genre permission
            Add the view_genre permission to the view_genre grp
            Add view_genre_staff to the view_genre group
        '''
        self.view_genre_grp = Group.objects.create(name = "View Genre")
        self.view_permissions = Permission.objects.filter(codename__in = ["view_genre"])
        self.view_genre_grp.permissions.set(self.view_permissions)
        view_genre_staff.groups.add(self.view_genre_grp)

        '''
            Create a grp for add_genre
            Get the add_genre permission
            Add the add_genre permission to the add_genre grp
            Add add_genre_staff to the add_genre group
        '''
        self.add_genre_grp = Group.objects.create(name = "Add Genre")
        self.add_permissions = Permission.objects.filter(codename__in = ["add_genre"])
        self.add_genre_grp.permissions.set(self.add_permissions)
        add_genre_staff.groups.add(self.add_genre_grp)

        res = self.client.post(self.login, {"username": "Thimmy", "password": "1234qwer"})
        self.admin_auth = res.data["access"]

        res = self.client.post(self.login, {"username": "thommy", "password": "1234qwer"})
        self.view_genre_auth = res.data["access"]

        res = self.client.post(self.login, {"username": "thiwo", "password": "1234qwer"})
        self.add_genre_auth = res.data["access"]


    def test_genre_get_api_without_credentials(self):
        res = self.client.get(self.list_create_genre)
        self.assertEqual(res.status_code, 401)


    def test_genre_view_api_with_wrong_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.add_genre_auth}")
        res = self.client.get(self.list_create_genre)
        self.assertEqual(res.status_code, 403)


    def test_genre_view_api_with_correct_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.view_genre_auth}")
        res = self.client.get(self.list_create_genre)
        self.assertEqual(res.status_code, 200)


    def test_genre_add_api_without_credentials(self):
        res = self.client.post(self.list_create_genre, data = {"genre": "thriller"})
        self.assertEqual(res.status_code, 401)


    def test_genre_add_api_with_wrong_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.view_genre_auth}")
        res = self.client.post(self.list_create_genre, data = {"genre": "thriller"})
        self.assertEqual(res.status_code, 403)


    def test_genre_add_api_with_correct_credentials(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_auth}")
        res = self.client.post(self.list_create_genre, data = {"genre": "thriiller"})
        self.assertEqual(res.status_code, 201)


    def test_genre_view_api_with_wrong_credential_after_switch(self):
        '''
            the grp perms will be switched for the 2 staffs and tested
            switch the permissions of add_genre grp from add_genre to view_genre
            switch the permissions of view_genre grp from add_genre to add_genre
            the users in the grps are not switched
            view_auth will be wrong for get request and add
        '''
        self.add_genre_grp.permissions.set(self.view_permissions)
        self.view_genre_grp.permissions.set(self.add_permissions)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.view_genre_auth}")
        res = self.client.get(self.list_create_genre)
        self.assertEqual(res.status_code, 403)


    def test_genre_add_api_with_wrong_credential_after_switch(self):
        '''
            the grp perms will be switched for the 2 staffs and tested
            switch the permissions of add_genre grp from add_genre to view_genre
            switch the permissions of view_genre grp from add_genre to add_genre
            the users in the grps are not switched
            view_auth will be wrong for get request and add
        '''
        self.add_genre_grp.permissions.set(self.view_permissions)
        self.view_genre_grp.permissions.set(self.add_permissions)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.add_genre_auth}")
        res = self.client.post(self.list_create_genre, data = {"genre": "Romance"})
        self.assertEqual(res.status_code, 403)

    def test_genre_view_api_with_correct_credential_after_switch(self):
        '''
            the grp perms will be switched for the 2 staffs and tested
            switch the permissions of add_genre grp from add_genre to view_genre
            switch the permissions of view_genre grp from add_genre to add_genre
            the users in the grps are not switched
            view_auth will be wrong for get request and add
        '''
        self.add_genre_grp.permissions.set(self.view_permissions)
        self.view_genre_grp.permissions.set(self.add_permissions)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.add_genre_auth}")
        res = self.client.get(self.list_create_genre)
        self.assertEqual(res.status_code, 200)


    def test_genre_add_api_with_correct_credential_after_switch(self):
        '''
            the grp perms will be switched for the 2 staffs and tested
            switch the permissions of add_genre grp from add_genre to view_genre
            switch the permissions of view_genre grp from add_genre to add_genre
            the users in the grps are not switched
            view_auth will be wrong for get request and add
        '''
        self.add_genre_grp.permissions.set(self.view_permissions)
        self.view_genre_grp.permissions.set(self.add_permissions)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.view_genre_auth}")
        res = self.client.post(self.list_create_genre, data = {"genre": "Action"})
        self.assertEqual(res.status_code, 201)

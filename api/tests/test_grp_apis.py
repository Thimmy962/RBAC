from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Staff
from django.contrib.auth.models import Permission, Group

class GroupTest(APITestCase):
    def setUp(self):
        self.token_url = reverse("token_obtain_pair")
        self.retrieve_role = reverse("retrieve_role", kwargs = {"pk": 2})
        self.list_create_role = reverse("list_create_role")
        self.list_create_staff = reverse("list_create_staff")
        self.retrieve_update_destroy_staff = reverse("retrieve_update_destroy_staff", kwargs = {"pk": 3})

        # create staffs
        self.admin_staff = Staff.objects.create_user(
            username="Admin",
            password="adminpass123",
            is_staff=True,
            is_superuser=True
        )

        manage_staff = Staff.objects.create_user(
            username = "Thimmy",
            password = "Uydnv1$1",
            is_staff=True
        )

        manage_grp = Staff.objects.create_user(
            username = "Thommy",
            password = "Uydnv1$1",
            is_staff=True
        )


        self.view_staff = Group.objects.create(name = "View Staffs")
        view_staff_permissions = Permission.objects.filter(codename__in=["view_staff"])
        self.view_staff.permissions.set(view_staff_permissions)
        manage_staff.groups.add(self.view_staff)


        self.view_grp = Group.objects.create(name = "Leader")
        view_grp_permissions = Permission.objects.filter(codename__in=["view_group"])
        self.view_grp.permissions.set(view_grp_permissions)
        manage_grp.groups.add(self.view_grp)


        # log in
        token_response = self.client.post(self.token_url, {
            "username": "admin",
            "password": "adminpass123"
        })
        self.superuser_access_token = token_response.data["access"]

        token_response = self.client.post(self.token_url, {
            "username": "thimmy",
            "password": "Uydnv1$1"
        })
        self.manage_staff_access_token = token_response.data["access"]

        
        token_response = self.client.post(self.token_url, {
            "username": "thommy",
            "password": "Uydnv1$1"
        })
        self.manage_grp_access_token = token_response.data["access"]

    def test_manage_grp_with_staff_cre(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_staff_access_token}")
        res = self.client.get(self.list_create_role)
        self.assertEqual(res.status_code, 403)

    def test_manage_stf_with_grp_cre(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.get(self.list_create_staff)
        self.assertEqual(res.status_code, 403)

    def test_manage_grp_with_authorized_cre_get_one_grp(self):
        # staff has view grp perm alone
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_staff_access_token}")
        res = self.client.get(self.retrieve_update_destroy_staff)
        self.assertEqual(res.status_code, 200)


    def test_manage_stf_with_unauthorized_cre_get(self):
        # staff has no grp perm for managing staffs
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.get(self.list_create_staff)
        self.assertEqual(res.status_code, 403)
    
    def test_manage_stf_with_authorized_cre_get(self):
        # staff has view staff
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_staff_access_token}")
        res = self.client.get(self.list_create_staff)
        self.assertEqual(res.status_code, 200)

    
    def test_manage_stf_with_authorized_cre_post(self):
        # staff has get staff perm for managing staff but want to post
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_staff_access_token}")
        res = self.client.post(self.list_create_staff, json = {"username": "leader", "password": "12345678"})
        self.assertEqual(res.status_code, 403)

    
    def test_manage_grp_with_authorized_cre_get(self):
        # staff has view grp perm alone
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.get(self.list_create_role)
        self.assertEqual(res.status_code, 200)

    def test_manage_grp_with_authorized_cre_get_one_grp(self):
        # staff has view grp perm alone
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.get(self.retrieve_role)
        self.assertEqual(res.status_code, 200)


    def test_manage_grp_with_unauthorized_cre_post(self):
        # staff has no grp perm for managing groups
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_staff_access_token}")
        res = self.client.post(self.list_create_role, json = {"name": "Leader", "permissions": [1,2,3,4,5]})
        self.assertEqual(res.status_code, 403)

    
    def test_manage_grp_with_athorized_cre_post(self):
        # staff has view grp perm alone but will try to create
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.post(self.list_create_role, json = {"name": "Leaders", "permissions": [1,2,3,4,5]})
        self.assertEqual(res.status_code, 403)

    def test_manage_grp_with_authorized_cre_post_permission_added(self):
        # staff has view grp perm alone  but staff grp will now be granted post perm
        post_grp = Permission.objects.get(codename="add_group")
        self.view_grp.permissions.add(post_grp.id)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.post(self.list_create_role,  data = {"name": "newjLeader", "permissions": [1,2,3,4,5]})
        self.assertEqual(res.status_code, 201)

    def test_manage_grp_with_authorized_cre_get_with_wrong_detail(self):
        # staff has view grp perm alone  but staff grp will now be granted post perm
        # will try to create grp with wrong detail hell
        post_grp = Permission.objects.get(codename="add_group")
        self.view_grp.permissions.add(post_grp.id)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.manage_grp_access_token}")
        res = self.client.post(self.list_create_role,  json = {"name": "Leaders", "hell": "", "permissions": [1,2,3,4,5]})
        self.assertEqual(res.status_code, 400)

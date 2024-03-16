from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ApplicantModel


class ApplicantTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user", "user@test.com", "password")

        self.view_applicant = Permission.objects.get(codename="view_applicant")
        self.create_applicant = Permission.objects.get(codename="create_applicant")
        self.update_applicant = Permission.objects.get(codename="update_applicant")
        self.delete_applicant = Permission.objects.get(codename="delete_applicant")

        self.data = {
            "first_name": "Spike",
            "last_name": "Spiegel",
            "email": "spike.spiegel@bebop.com",
            "phone_number": "123-456-7890",
            "address": "123 Cowboy Pl",
            "zip_code": "10000",
            "state": "New York",
        }

    def test_list_applicants(self):
        applicant = ApplicantModel.objects.create(**self.data)
        applicant.save()

        self.user.user_permissions.set([self.view_applicant])
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/applicant/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertGreaterEqual(dict(response.data[0]).items(), self.data.items())

    def test_create_applicant(self):
        self.user.user_permissions.set([self.create_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/applicant/", self.data, format="json")
        applicant = ApplicantModel.objects.get()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ApplicantModel.objects.count(), 1)
        self.assertEqual(applicant.first_name, "Spike")
        self.assertEqual(applicant.last_name, "Spiegel")
        self.assertEqual(applicant.email, "spike.spiegel@bebop.com")
        self.assertEqual(applicant.phone_number, "123-456-7890")
        self.assertEqual(applicant.address, "123 Cowboy Pl")
        self.assertEqual(applicant.zip_code, "10000")
        self.assertEqual(applicant.state, "New York")

    def test_view_applicant_details(self):
        applicant = ApplicantModel.objects.create(**self.data)
        applicant.save()

        self.user.user_permissions.set([self.view_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.get(f"/api/applicant/{applicant.id}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Spike")
        self.assertEqual(response.data["last_name"], "Spiegel")
        self.assertEqual(response.data["email"], "spike.spiegel@bebop.com")
        self.assertEqual(response.data["phone_number"], "123-456-7890")
        self.assertEqual(response.data["address"], "123 Cowboy Pl")
        self.assertEqual(response.data["zip_code"], "10000")
        self.assertEqual(response.data["state"], "New York")

    def test_update_applicant_status(self):
        applicant = ApplicantModel.objects.create(**self.data)
        applicant.save()

        self.user.user_permissions.set([self.update_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.put(
            f"/api/applicant/{applicant.id}/",
            {"status": "APPROVED"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ApplicantModel.objects.get().status, "APPROVED")

    def test_delete_applicant(self):
        applicant = ApplicantModel.objects.create(**self.data)
        applicant.save()

        self.user.user_permissions.set([self.delete_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.delete(f"/api/applicant/{applicant.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ApplicantModel.objects.count(), 0)

    def test_get_empty_applicant_list(self):
        self.user.user_permissions.set([self.view_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/applicant/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_returns_status_code_400_with_invalid_data(self):
        self.user.user_permissions.set([self.create_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/applicant/", {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_request_for_nonexistent_applicant_should_return_400(self):
        self.user.user_permissions.set([self.view_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.get("/api/applicant/1/", format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_status_code_400_on_invalid_put_request(self):
        applicant = ApplicantModel.objects.create(**self.data)
        applicant.save()

        self.user.user_permissions.set([self.update_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.put(
            f"/api/applicant/{applicant.id}/",
            {"status": "BEEF"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_status_code_400_for_nonexistent_applicant_on_put_request(self):
        self.user.user_permissions.set([self.update_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.put(
            "/api/applicant/1/",
            {"status": "ACCEPTED"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_status_code_400_for_nonexistent_applicant_on_delete_request(self):
        self.user.user_permissions.set([self.delete_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.delete("/api/applicant/1/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_return_status_403_for_list_applicants_withouth_auth(self):
        response = self.client.get("/api/applicant/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_create_applicant_withouth_auth(self):
        response = self.client.post("/api/applicant/", self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_view_applicant_withouth_auth(self):
        response = self.client.get("/api/applicant/1/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_update_applicant_status_withouth_auth(self):
        response = self.client.put(
            "/api/applicant/1/",
            {"status": "APPROVED"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_delete_applicant_withouth_auth(self):
        response = self.client.delete("/api/applicant/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_list_applicants_with_incorrect_permission(self):
        self.user.user_permissions.set(
            [self.create_applicant, self.update_applicant, self.delete_applicant]
        )
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/applicant/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_create_applicant_with_incorrect_permission(self):
        self.user.user_permissions.set(
            [self.view_applicant, self.update_applicant, self.delete_applicant]
        )
        self.client.force_authenticate(self.user)
        response = self.client.post("/api/applicant/", self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_view_applicant_with_incorrect_permission(self):
        self.user.user_permissions.set(
            [self.create_applicant, self.update_applicant, self.delete_applicant]
        )
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/applicant/1/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_update_applicant_status_with_incorrect_permission(
        self,
    ):
        self.user.user_permissions.set(
            [self.view_applicant, self.create_applicant, self.delete_applicant]
        )
        self.client.force_authenticate(self.user)
        response = self.client.put(
            "/api/applicant/1/",
            {"status": "APPROVED"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_delete_applicant_with_incorrect_permission(self):
        self.user.user_permissions.set(
            [
                self.view_applicant,
                self.create_applicant,
                self.update_applicant,
            ]
        )
        self.client.force_authenticate(self.user)
        response = self.client.delete("/api/applicant/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

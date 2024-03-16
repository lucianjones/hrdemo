import pytest
import logging

from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from api.models import ApplicantModel
from api.views import ApplicantDetailApiView, ApplicantListApiView

logger = logging.getLogger(__name__)


class ApplicantDetailTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user("test_user", "user@test.com", "password")
        self.view_applicant = Permission.objects.get(codename="view_applicant")
        self.create_applicant = Permission.objects.get(codename="create_applicant")
        self.update_applicant = Permission.objects.get(codename="update_applicant")
        self.delete_applicant = Permission.objects.get(codename="delete_applicant")
        self.view_note = Permission.objects.get(codename="view_note")
        self.create_note = Permission.objects.get(codename="create_note")

    def test_create_applicant(self):
        data = {
            "first_name": "Spike",
            "last_name": "Spiegel",
            "email": "spike.spiegel@bebop.com",
            "phone_number": "123-456-7890",
            "address": "123 Cowboy Pl",
            "zip_code": "10000",
            "state": "New York",
        }

        self.user.user_permissions.set([self.create_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.post("/api/applicant/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ApplicantModel.objects.count(), 1)
        self.assertEqual(ApplicantModel.objects.get().first_name, "Spike")

    def test_list_applicants(self):
        data = {
            "first_name": "Spike",
            "last_name": "Spiegel",
            "email": "spike.spiegel@bebop.com",
            "phone_number": "123-456-7890",
            "address": "123 Cowboy Pl",
            "zip_code": "10000",
            "state": "New York",
        }

        applicant = ApplicantModel.objects.create(**data)
        applicant.save()

        self.user.user_permissions.set([self.view_applicant])
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/applicant/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertGreaterEqual(dict(response.data[0]).items(), data.items())

        logger.info(len(response.data[0]))



# @pytest.mark.django_db
# def test_create_applicant(factory) -> None:
#     """
#     Test the create applicant API
#     :param factory:
#     :return: None
#     """
#     payload = {
#         "first_name": "Spike",
#         "last_name": "Spiegel",
#         "email": "spike.spiegel@bebop.com",
#         "phone_number": "123-456-7890",
#         "address": "123 Cowboy Pl",
#         "zip_code": "10000",
#         "state": "New York",
#     }

#     test_user = User.objects.create_user("test_user", "user@test.com", "password")

#     view_applicant = Permission.objects.get(codename="view_applicant")
#     create_applicant = Permission.objects.get(codename="create_applicant")
#     update_applicant = Permission.objects.get(codename="update_applicant")
#     delete_applicant = Permission.objects.get(codename="delete_applicant")
#     view_note = Permission.objects.get(codename="view_note")
#     create_note = Permission.objects.get(codename="create_note")

#     test_user.user_permissions.add(
#         view_applicant,
#         create_applicant,
#     )

#     applicant_detail_view = ApplicantDetailApiView.as_view()
#     applicant_list_view = ApplicantListApiView.as_view()

#     create_request = factory.post("/api/applicant/", data=payload, format="json")
#     force_authenticate(create_request, user=test_user)
#     create_response = applicant_list_view(create_request)
#     logger.info(f"Response: {create_response.data}")
#     applicant_uuid = create_response.data["uuid"]
#     logger.info(f"Created applicant with id: {applicant_uuid}")
#     assert create_response.status_code == 201
#     assert create_response.data["first_name"] == payload["first_name"]

#     read_request = factory.get(
#         f"/api/applicant/{applicant_uuid}/", uuid=applicant_uuid, format="json"
#     )
#     force_authenticate(read_request, user=test_user)
#     read_response = applicant_detail_view(read_request)
#     logger.info(f"Response: {read_response.data}")
#     assert read_response.status_code == 200
#     assert read_response.data["first_name"] == payload["first_name"]

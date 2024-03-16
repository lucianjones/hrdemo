from django.contrib.auth.models import Permission, User
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import ApplicantModel, NoteModel


class NoteTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("test_user", "user@test.com", "password")

        self.view_note = Permission.objects.get(codename="view_note")
        self.create_note = Permission.objects.get(codename="create_note")
        self.delete_applicant = Permission.objects.get(codename="delete_applicant")

        self.applicant_data = {
            "first_name": "Spike",
            "last_name": "Spiegel",
            "email": "spike.spiegel@bebop.com",
            "phone_number": "123-456-7890",
            "address": "123 Cowboy Pl",
            "state": "New York",
        }

        self.note_data = {
            "title": "This is a note",
            "content": "This is the body of a note",
        }

    def test_list_notes(self):
        applicant = ApplicantModel.objects.create(**self.applicant_data)
        applicant.save()

        note = NoteModel.objects.create(applicant=applicant, **self.note_data)
        note.save()

        self.user.user_permissions.set([self.view_note])
        self.client.force_authenticate(self.user)

        response = self.client.get(
            f"/api/applicant/{applicant.id}/note/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertGreaterEqual(dict(response.data[0]).items(), self.note_data.items())

    def test_create_note(self):
        applicant = ApplicantModel.objects.create(**self.applicant_data)
        applicant.save()

        self.user.user_permissions.set([self.create_note])
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f"/api/applicant/{applicant.id}/note/", data=self.note_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NoteModel.objects.count(), 1)
        self.assertEqual(response.data["title"], self.note_data["title"])
        self.assertEqual(response.data["content"], self.note_data["content"])
        self.assertEqual(response.data["applicant"], applicant.id)

    def test_get_empty_note_list(self):
        applicant = ApplicantModel.objects.create(**self.applicant_data)
        applicant.save()

        self.user.user_permissions.set([self.view_note])
        self.client.force_authenticate(self.user)

        response = self.client.get(
            f"/api/applicant/{applicant.id}/note/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_create_returns_status_code_400_with_invalid_data(self):
        applicant = ApplicantModel.objects.create(**self.applicant_data)
        applicant.save()

        self.user.user_permissions.set([self.create_note])
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f"/api/applicant/{applicant.id}/note/", data={}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_note_invalid_applicant(self):
        invalid_applicant_id = 9999

        self.user.user_permissions.set([self.create_note])
        self.client.force_authenticate(self.user)

        response = self.client.post(
            f"/api/applicant/{invalid_applicant_id}/note/",
            data=self.note_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Deleting an existing applicant also deletes associated notes

    def test_delete_applicant_deletes_notes(self):
        applicant = ApplicantModel.objects.create(**self.applicant_data)
        applicant.save()

        note = NoteModel.objects.create(applicant=applicant, **self.note_data)
        note.save()

        self.user.user_permissions.set([self.delete_applicant])
        self.client.force_authenticate(self.user)

        response = self.client.delete(f"/api/applicant/{applicant.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(NoteModel.objects.count(), 0)

    def test_return_status_403_for_list_notes_withouth_auth(self):
        response = self.client.get("/api/applicant/1/note/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_create_notes_withouth_auth(self):
        response = self.client.post(
            "/api/applicant/1/note/", self.note_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_list_notes_with_incorrect_permission(self):
        self.user.user_permissions.set([self.create_note])
        self.client.force_authenticate(self.user)
        response = self.client.get("/api/applicant/1/note/", format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_return_status_403_for_create_note_with_incorrect_permission(self):
        self.user.user_permissions.set([self.view_note])
        self.client.force_authenticate(self.user)
        response = self.client.post(
            "/api/applicant/1/note/", self.note_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

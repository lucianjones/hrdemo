from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import ApplicantModel, NoteModel
from api.permissions import ApplicantPermissions, NotePermissions
from api.serializers import ApplicantSerializer, NoteSerializer


class ApplicantListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ApplicantPermissions]

    def get(self, request, *args, **kwargs):
        """
        Return all ApplicantModels
        """
        applicants = ApplicantModel.objects.all()
        serializer = ApplicantSerializer(applicants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """
        Create an ApplicantModel
        """
        data = {
            "first_name": request.data.get("first_name"),
            "last_name": request.data.get("last_name"),
            "email": request.data.get("email"),
            "phone_number": request.data.get("phone_number"),
            "address": request.data.get("address"),
            "zip_code": request.data.get("zip_code"),
            "state": request.data.get("state"),
        }
        serializer = ApplicantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicantDetailApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ApplicantPermissions]

    def get_object(self, id):
        """
        Helper method to get the object with id
        """
        try:
            return ApplicantModel.objects.get(id=id)
        except ApplicantModel.DoesNotExist:
            return None

    def get(self, request, id: int, *args, **kwargs):
        """
        Retrieves the ApplicantModel with given id
        """
        applicant_instance = self.get_object(id)
        if not applicant_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ApplicantSerializer(applicant_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id: int, *args, **kwargs):
        """
        Updates the ApplicantModel with given id if exists
        """
        applicant_instance = self.get_object(id)
        if not applicant_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {"status": request.data.get("status")}
        serializer = ApplicantSerializer(
            instance=applicant_instance, data=data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id: int, *args, **kwargs):
        """
        Deletes the ApplicantModel with given id if exists
        """
        applicant_instance = self.get_object(id)
        if not applicant_instance:
            return Response(
                {"res": "Object with id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        applicant_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)


class ApplicantNoteListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, NotePermissions]

    def get(self, request, id: int, *args, **kwargs):
        """
        Return all NoteModels associated with the ApplicantModel of the given
        id
        """
        applicant_notes = NoteModel.objects.filter(applicant__id=id)
        serializer = NoteSerializer(applicant_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id: int, *args, **kwargs):
        """
        Creates a NoteModel associated with the ApplicantModel of the given
        id
        """
        data = {
            "applicant": id,
            "title": request.data.get("title"),
            "content": request.data.get("content"),
        }
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

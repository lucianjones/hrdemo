from rest_framework import serializers

from api.models import ApplicantModel, NoteModel


class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantModel
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteModel
        fields = "__all__"
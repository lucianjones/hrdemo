from django.db import models
from uuid import uuid4


class ApplicantModel(models.Model):
    class Meta:
        permissions = [
            ("view_applicant", "Can view one or many applicants"),
            ("create_applicant", "Can create applicants"),
            ("update_applicant", "Can update applicants"),
            ("delete_applicant", "Can delete applicants"),
        ]

    class ApplicantStatus(models.TextChoices):
        PENDING = "PENDING"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"

    uuid = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid4,
        editable=False,
        unique=True,
    )

    first_name = models.CharField(max_length=256, blank=False)
    last_name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(unique=True, blank=False, max_length=256)
    phone_number = models.CharField(max_length=20, blank=False)
    address = models.CharField(max_length=256, blank=False)
    zip_code = models.CharField(max_length=20, blank=False)
    state = models.CharField(max_length=50, blank=False)
    status = models.CharField(
        max_length=8,
        choices=ApplicantStatus.choices,
        default=ApplicantStatus.PENDING,
    )

    def __str__(self):
        return f"({self.uuid}) {self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class NoteModel(models.Model):
    class Meta:
        permissions = [
            ("view_note", "Can view one or many applicants"),
            ("create_note", "Can create applicants"),
        ]

    uuid = models.UUIDField(
        primary_key=True,
        db_index=True,
        default=uuid4,
        editable=False,
        unique=True,
    )

    applicant = models.ForeignKey(ApplicantModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.TextField()

    def __str__(self):
        return f"{self.applicant.full_name} - {self.title}"

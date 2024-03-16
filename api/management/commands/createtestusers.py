from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here
        allperms = User.objects.create_user(
            "allperms", "user0@test.com", "password"
        )
        viewapplicant = User.objects.create_user(
            "viewapplicant", "user1@test.com", "password"
        )
        createapplicant = User.objects.create_user(
            "createapplicant", "user2@test.com", "password"
        )
        updateapplicant = User.objects.create_user(
            "updateapplicant", "user3@test.com", "password"
        )
        deleteapplicant = User.objects.create_user(
            "deleteapplicant", "user4@test.com", "password"
        )
        viewnote = User.objects.create_user(
            "viewnote", "user5@test.com", "password"
        )
        createnote = User.objects.create_user(
            "createnote", "user6@test.com", "password"
        )
        view_applicant = Permission.objects.get(codename="view_applicant")
        create_applicant = Permission.objects.get(codename="create_applicant")
        update_applicant = Permission.objects.get(codename="update_applicant")
        delete_applicant = Permission.objects.get(codename="delete_applicant")
        view_note = Permission.objects.get(codename="view_note")
        create_note = Permission.objects.get(codename="create_note")

        allperms.user_permissions.add(
            view_applicant,
            create_applicant,
            update_applicant,
            delete_applicant,
            view_note,
            create_note,
        )
        viewapplicant.user_permissions.add(view_applicant)
        createapplicant.user_permissions.add(create_applicant)
        updateapplicant.user_permissions.add(update_applicant)
        deleteapplicant.user_permissions.add(delete_applicant)
        viewnote.user_permissions.add(delete_applicant)
        createnote.user_permissions.add(delete_applicant)

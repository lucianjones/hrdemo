from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        # now do the things that you want with your models here
        user0 = User.objects.create_user(
            "user0", "user0@test.com", "password"
        )
        user1 = User.objects.create_user(
            "user1", "user1@test.com", "password"
        )
        user2 = User.objects.create_user(
            "user2", "user2@test.com", "password"
        )
        user3 = User.objects.create_user(
            "user3", "user3@test.com", "password"
        )
        user4 = User.objects.create_user(
            "user4", "user4@test.com", "password"
        )
        view_applicant = Permission.objects.get(codename="view_applicant")
        create_applicant = Permission.objects.get(codename="create_applicant")
        update_applicant = Permission.objects.get(codename="update_applicant")
        delete_applicant = Permission.objects.get(codename="delete_applicant")
        view_note = Permission.objects.get(codename="view_note")
        create_note = Permission.objects.get(codename="create_note")

        user0.user_permissions.add(
            view_applicant,
            create_applicant,
            update_applicant,
            delete_applicant,
            view_note,
            create_note,
        )
        user1.user_permissions.add(view_applicant)
        user2.user_permissions.add(create_applicant)
        user3.user_permissions.add(update_applicant)
        user4.user_permissions.add(delete_applicant)

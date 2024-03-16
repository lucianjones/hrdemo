from django.contrib.auth.models import Permission, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        User.objects.get(email="user0@test.com").delete()
        User.objects.get(email="user1@test.com").delete()
        User.objects.get(email="user2@test.com").delete()
        User.objects.get(email="user3@test.com").delete()
        User.objects.get(email="user4@test.com").delete()
        User.objects.get(email="user5@test.com").delete()
        User.objects.get(email="user6@test.com").delete()


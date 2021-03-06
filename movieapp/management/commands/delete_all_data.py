from django.contrib.auth.models import User
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone

from movieapp.models import MotionPicture as mp


class Command(BaseCommand):
    help = 'Delete all Users and Movies'
    def handle(self, *args, **kwargs):

        users = User.objects.all()
        movies = mp.objects.all()
        for movie in movies:
            self.stdout.write('Deleting movie {}'.format(movie.name))
            movie.delete()
        for user in users:
            self.stdout.write('Deleting user {}'.format(user.username))
            user.delete()

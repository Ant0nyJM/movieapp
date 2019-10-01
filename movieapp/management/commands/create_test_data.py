from django.contrib.auth.models import User
from movieapp.models import MotionPicture as mp
from django.utils import timezone
from django.core.files import File
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Creates User and Movies'
    def handle(self, *args, **kwargs):

        ad = User(username='admin')
        ad.set_password('admin')
        ad.email = 'admin@email.com'
        ad.is_staff = True
        ad.is_superuser = True
        ad.save()
        self.stdout.write("User Created {}".format(ad.username))

        test1 = User(username='test1')
        test1.set_password('asdf')
        test1.email = 'test1@email.com'
        test1.is_active = True
        test1.save()
        self.stdout.write("User Created {}".format(test1.username))

        test2 = User(username='test2')
        test2.set_password('asdf')
        test2.email = 'test2@email.com'
        test2.is_active = True
        test2.save()
        self.stdout.write("User Created {}".format(test2.username))


        mv = mp(name='Mad Max',genre='Action',release_date=timezone.now().date(),description="Apocalypse",user = test1,approved=True)
        mv.image.save('mad_max.jpg',File(open('/home/sayone/Desktop/mad_max.jpg','rb')))
        mv.save()
        self.stdout.write("Movie Created {}".format(mv.name))


        mv = mp(name='Avatar',genre='Adventure',release_date=timezone.now().date(),description="Aliens",user = test1,approved=True)
        mv.image.save('avataar.jpg',File(open('/home/sayone/Desktop/avataar.jpg','rb')))
        mv.save()
        self.stdout.write("Movie Created {}".format(mv.name))

        mv = mp(name='Fight Club',genre='Psychological',release_date=timezone.now().date(),description="Alter Ego",user = test1,approved=True)
        mv.image.save('fc.jpg',File(open('/home/sayone/Desktop/fight_club.jpg','rb')))
        mv.save()
        self.stdout.write("Movie Created {}".format(mv.name))

        mv = mp(name='Hacksaw Ridge',genre='Military',release_date=timezone.now().date(),description="War",user = test2,approved=True)
        mv.image.save('hacksaw.jpeg',File(open('/home/sayone/Desktop/hacksaw.jpeg','rb')))
        mv.save()
        self.stdout.write("Movie Created {}".format(mv.name))

        mv = mp(name='Jaws',genre='Horror',release_date=timezone.now().date(),description="Shark",user = test2,approved=True)
        mv.image.save('jaws.jpg',File(open('/home/sayone/Desktop/jaws.jpg','rb')))
        mv.save()
        self.stdout.write("Movie Created {}".format(mv.name))





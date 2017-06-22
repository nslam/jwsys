from django.core.management.base import BaseCommand, CommandError
from basicInfo import *
from django.contrib.auth.models import User
from basicInfo.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        user = User.objects.create_user(options['name'][0], None, options['name'][1])
        Instructor.objects.create(user=user, gender=1)
        print('Creating instructor successfully!')
        print('Your account is:', options['name'][0])
        print('Your password is:', options['name'][1])

from django.core.management.base import BaseCommand, CommandError
from basicInfo import *
from django.contrib.auth.models import User
from basicInfo.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('name', nargs='+', type=str)

    def handle(self, *args, **options):
        Department.objects.create(name=options['name'][0], building=options['name'][1])
        print('Creating department successfully!')
        print('The name is:', options['name'][0])
        print('The building is:', options['name'][1])

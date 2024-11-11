# yourapp/management/commands/setup_site.py
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Sets up the site domain for Render deployment'

    def handle(self, *args, **kwargs):
        site = Site.objects.get_or_create(id=2)[0]  # Changed from 1 to 2
        site.domain = 'asha2.onrender.com'
        site.name = 'asha2.onrender.com'
        site.save()
        self.stdout.write(self.style.SUCCESS('Successfully set up site domain'))

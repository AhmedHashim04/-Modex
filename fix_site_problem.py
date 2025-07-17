# python manage.py shell
from django.contrib.sites.models import Site
Site.objects.filter(id=1).update(domain='127.0.0.1:8000', name='Localhost')

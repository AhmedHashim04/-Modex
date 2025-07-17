
from product.models import Product 

from django.contrib.auth.decorators import login_required
from .models import  Collection
from django.contrib import messages
from django.utils.translation import gettext as _
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'features/collection_detail.html'
    context_object_name = 'collection'
    slug_field = "slug"
    slug_url_kwarg = "slug"


# import django_filters
# from .models import Product
# from django.db.models import Q

# class ProductFilter(django_filters.FilterSet):
#     search = django_filters.CharFilter(method='filter_search', label='Search')
#     min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
#     max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
#     tag = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
#     category = django_filters.CharFilter(method='filter_category')

#     class Meta:
#         model = Product
#         fields = ['search', 'min_price', 'max_price', 'tag', 'category']

#     def filter_search(self, queryset, name, value):
#         return queryset.filter(
#             Q(name__icontains=value) |
#             Q(description__icontains=value) |
#             Q(category__name__icontains=value)
#         )

#     def filter_category(self, queryset, name, value):
#         return queryset.filter(
#             Q(category__slug=value) |
#             Q(category__parent__slug=value)
#         )

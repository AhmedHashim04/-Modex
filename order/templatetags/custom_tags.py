from django import template

register = template.Library()

@register.filter
def get_item(queryset, pk):
    try:
        return queryset.get(pk=pk)
    except:
        return None


@register.filter
def get_index(queryset, index):
    try:
        return list(queryset)[index]
    except:
        return None




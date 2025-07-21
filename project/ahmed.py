from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='2/m', block=False)
@require_GET
def test_limit(request):
    if getattr(request, 'limited', False):
        return JsonResponse({'error': 'Too many requests'}, status=429)
    return JsonResponse({'message': 'OK'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from banners.models import Banner


def banners_list_api(request):
    banners = Banner.objects.filter(is_active=True)
    dumped_banners = []
    for banner in banners:
        dumped_banners.append({
            'title': banner.title,
            'src': banner.image.url,
            'text': banner.text,
            'slug': banner.slug,
        })

    return JsonResponse(dumped_banners, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['GET'])
def get_banner(request, banner_slug):
    banner = get_object_or_404(Banner, slug=banner_slug)
    return Response({
        'title': banner.title,
        'src': banner.image.url,
        'text': banner.text,
        'slug': banner.slug,
    })

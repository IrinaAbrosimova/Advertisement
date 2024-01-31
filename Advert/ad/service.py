from django_filters import rest_framework as filters
from .models import Ad


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class AdFilter(filters.FilterSet):
    category = CharFilterInFilter(field_name='category__name', lookup_expr='in')
    published_date = filters.RangeFilter()

    class Meta:
        model = Ad
        fields = ['category', 'published_date']


import django_filters

from accounts_shared.models import (
    BusinessClientContact
)


class BusinessClientContactFilter(django_filters.FilterSet):
    account = django_filters.NumberFilter(
        field_name='account', lookup_expr='exact')

    class Meta:
        model = BusinessClientContact
        fields = ['account']

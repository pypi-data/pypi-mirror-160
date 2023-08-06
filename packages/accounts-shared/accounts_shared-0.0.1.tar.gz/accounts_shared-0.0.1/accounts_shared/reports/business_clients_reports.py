from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
import decimal
from django.db.models import Sum, F, Q, Count
from django.db.models import Value as V
from django.db.models.functions import Concat
from datetime import datetime
from rest_framework.views import APIView

from accounts_shared.models import BusinessClient, ConsumerClient
from dateutil.relativedelta import relativedelta
from django.db.models import Case, Value, When


class BusinessClientsByCityView(APIView):
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        result = (BusinessClient.objects.annotate(addresses_count=Count('addresses')).filter(addresses_count__gt=0)
                  .values('addresses__city__name')
                  .annotate(name=F('addresses__city__name'), value=Count('addresses__city')).values('name', 'value')
                  .order_by()
                  )
        print(result)

        return Response(result, status=status.HTTP_200_OK)

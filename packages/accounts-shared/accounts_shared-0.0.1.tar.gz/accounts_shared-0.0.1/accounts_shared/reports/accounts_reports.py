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

from accounts_shared.models import ConsumerClient
from dateutil.relativedelta import relativedelta
from django.db.models import Case, Value, When


class ConsumerClientsByAgeView(APIView):
    authentication_classes = (TokenAuthentication,)

    range_ages = (
        {"lookup": "gte", "label": "<17", "age": [18]},
        {"lookup": "range", "label": "18-24", "age": [18, 25]},
        {"lookup": "range", "label": "25-34", "age": [25, 35]},
        {"lookup": "range", "label": "35-44", "age": [35, 45]},
        {"lookup": "range", "label": "45-54", "age": [45, 55]},
        {"lookup": "range", "label": "55-64", "age": [55, 65]},
        {"lookup": "lt", "label": ">65", "age": [65]},
    )

    def get(self, request):
        consumer_clients = ConsumerClient.objects.all()
        aggr_query = {}
        current_date = datetime.now().date()

        for item in self.range_ages:
            age = item.get("age")
            lookup = item.get("lookup")
            label = item.get("label")
            # calculate start_date an end_date
            end_date = current_date - relativedelta(years=age[0])
            start_date = current_date - relativedelta(years=age[-1], days=-1)
            f_value = start_date if len(age) == 1 else (start_date, end_date)
            if lookup == "gte":
                aggr_query[label] = Count(
                    Case(When(dateOfBirth__gte=f_value, then=1)))
            elif lookup == "lt":
                aggr_query[label] = Count(
                    Case(When(dateOfBirth__lt=f_value, then=1)))
            else:
                aggr_query[label] = Count(
                    Case(When(dateOfBirth__range=f_value, then=1)))

        # Aggregate values
        qs_values = ConsumerClient.objects.all().aggregate(**aggr_query)
        result = []
        print(qs_values)
        for key, value in qs_values.items():
            item = {}
            item["name"] = key
            item["value"] = value
            result.append(item)
        return Response(result, status=status.HTTP_200_OK)

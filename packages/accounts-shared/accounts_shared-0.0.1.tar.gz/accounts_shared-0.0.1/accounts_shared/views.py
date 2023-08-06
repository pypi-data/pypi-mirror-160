import requests
# from users.models import (CustomUser)
from accounts_shared.filters.filters import BusinessClientContactFilter
from team_common.models import User
from .models import (Supplier, SupplierCategory, ShippingAddress, BillingAddress, Country,
                     ConsumerClient, BusinessClient, Contact, Account, Address, Company,
                     City, CompanyLocation,
                     SupplierContact, BusinessClientContact,
                     CertificationEntity, TestAccount,
                     )
from .serializers import (SupplierSerializer, SupplierCategorySerializer,
                          AddressSerializer,
                          CountrySerializer, BillingAddressSerializer, ConsumerClientSerializer,
                          ConsumerClientReadSerializer, BusinessClientSerializer,
                          BusinessClientReadSerializer, ContactSerializer, ContactReadSerializer,
                          AccountReadSerializer, AccountSerializer, AddressReadSerializer,
                          SupplierReadSerializer, CompanySerializer, CompanyReadSerializer,
                          AllClientSerializer,
                          CitySerializer,
                          CompanyLocationSerializer, CompanyLocationReadSerializer,
                          CertificationEntitySerializer,
                          CertificationEntityReadSerializer,
                          ShippingAddressSerializer,
                          ShippingAddressReadSerializer,
                          SupplierContactSerializer,
                          SupplierContactReadSerializer,
                          BusinessClientContactSerializer,
                          BusinessClientContactReadSerializer,
                          TestAccountSerializer
                          )
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import action
import itertools
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
import django_filters
from rest_framework import generics
from django.db.models import Q
from django_filters.views import FilterView


class BookAnAppointmentSearchCompanyLocationsFilterSet(django_filters.FilterSet):
    location = django_filters.CharFilter(method='filter_q')
    # postalCode = django_filters.CharFilter(field_name="address__postalCode")

    def filter_q(self, qs, name, value):
        return qs.filter(
            Q(address__city__name__icontains=value) | Q(address__postalCode=value)
        )

    class Meta:
        model = CompanyLocation
        fields = ['address__city', 'address__postalCode']


class BookAnAppointmentSearchCompanyLocationsView(generics.ListAPIView, FilterView):
    serializer_class = CompanyLocationReadSerializer
    queryset = CompanyLocation.objects.all()
    permission_classes = [AllowAny]
    filterset_class = BookAnAppointmentSearchCompanyLocationsFilterSet


class CompanyLocationFilterSet(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name="address__city__id")

    class Meta:
        model = CompanyLocation
        fields = ['city']


class CompanyLocationViewSet(viewsets.ModelViewSet):
    filterset_class = CompanyLocationFilterSet

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompanyLocationReadSerializer
        return CompanyLocationSerializer
    queryset = CompanyLocation.objects.all()
    permission_classes = [AllowAny]


class AccountViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AccountReadSerializer
        return AccountSerializer
    queryset = Account.objects.all()
    authentication_classes = (TokenAuthentication,)

class CompanyViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CompanyReadSerializer
        return CompanySerializer
    queryset = Company.objects.all()
    authentication_classes = (TokenAuthentication,)

class MyCompanyView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        company = Company.objects.filter(
            email='henryhamamji@gmail.com')[0]
        serializer = CompanyReadSerializer(company, many=False, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    authentication_classes = [] 
    permission_classes = [AllowAny]

class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = [AllowAny]
    authentication_classes = [] 

class SupplierCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierCategorySerializer
    queryset = SupplierCategory.objects.all()
    authentication_classes = (TokenAuthentication,)

class BillingAddressViewSet(viewsets.ModelViewSet):
    serializer_class = BillingAddressSerializer
    queryset = BillingAddress.objects.all()
    authentication_classes = (TokenAuthentication,)


class ShippingAddressViewSet(viewsets.ModelViewSet):
    queryset = ShippingAddress.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShippingAddressReadSerializer
        return ShippingAddressSerializer

class AddressViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AddressReadSerializer
        return AddressSerializer
    queryset = Address.objects.all()
    authentication_classes = (TokenAuthentication,)
    
    def create(self, request):
        data = request.data
        country_id = data.pop('country', None)
        city_id = data.pop('city', None)
        account_id = data.pop('account')
        address = Address.objects.create(
            **data,
            country_id=country_id,
            city_id=city_id,
            account_id=account_id
        )
        serializer = AddressReadSerializer(address, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ShippingAddressesByAccountList(generics.ListAPIView):

    def get_queryset(self):
        queryset = ShippingAddress.objects.all()
        account_id = self.request.query_params.get('account', None)
        if account_id is not None:
            queryset = queryset.filter(account__id=account_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShippingAddressReadSerializer
        return ShippingAddressSerializer
    authentication_classes = (TokenAuthentication,)

class AddressesByAccountList(generics.ListAPIView):

    def get_queryset(self):
        queryset = Address.objects.all()
        account_id = self.request.query_params.get('account', None)
        if account_id is not None:
            queryset = queryset.filter(account__id=account_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return AddressReadSerializer
        return AddressSerializer
    authentication_classes = (TokenAuthentication,)

class CertificationEntityViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CertificationEntityReadSerializer
        return CertificationEntitySerializer
    queryset = CertificationEntity.objects.all()
    authentication_classes = (TokenAuthentication,)

class SupplierViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierReadSerializer
        return SupplierSerializer
    queryset = Supplier.objects.all()
    authentication_classes = (TokenAuthentication,)

    def get_country(self, request):
        country_data = request.data['address']['country']
        countryId = country_data['id']
        country = Country.objects.get(id=countryId)
        return country

    def create_address(self, request):
        addressLine1 = request.data['address']['addressLine1']
        region = request.data['address']['region']
        city = request.data['address']['city']
        postalCode = request.data['address']['postalCode']
        country = self.get_country(request)
        address = Address.objects.create(
            addressLine1=addressLine1, region=region, city=city, postalCode=postalCode, country=country)
        return address

    @action(detail=False, methods=['POST'])
    def add_supplier(self, request, pk=None):
        if request.data:
            supplierCategoryData = request.data['supplierCategories']
            supplierCategoryIds = [category['id']
                                   for category in supplierCategoryData]
            supplierCategories = SupplierCategory.objects.filter(
                id__in=supplierCategoryIds)
            companyName = request.data['companyName']
            website = request.data['website']
            contactName = request.data['contactName']
            contactEmail = request.data['contactEmail']
            contactPhoneNumber = request.data['contactPhoneNumber']
            newAddress = self.create_address(request)
            supplier = Supplier.objects.create(address=newAddress, companyName=companyName, contactName=contactName,
                                               contactEmail=contactEmail, website=website, contactPhoneNumber=contactPhoneNumber)
            supplier.supplierCategories.set(supplierCategories)
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'new supplier added',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide supplier data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_contact_name(self, request, pk=None):
        if request.data:
            supplier = Supplier.objects.get(id=pk)
            supplier.contactName = request.data['contactName']
            supplier.save()
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'supplier contact name was changed',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide supplier contact name'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_contact_email(self, request, pk=None):
        if request.data:
            supplier = Supplier.objects.get(id=pk)
            supplier.contactEmail = request.data['contactEmail']
            supplier.save()
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'supplier contact email was changed',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'you need to provide supplier contact email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_contact_phone_number(self, request, pk=None):
        if request.data:
            supplier = Supplier.objects.get(id=pk)
            supplier.contactEmail = request.data['contactPhoneNumber']
            supplier.save()
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'supplier contact phone number was changed',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'you need to provide supplier contact phone number'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_supplier_categories(self, request, pk=None):
        if request.data:
            supplier = Supplier.objects.get(id=pk)
            supplier_categories_data = request.data['supplierCategories']
            new_supplier_categories = []
            for supplierCategory in supplier_categories_data:
                new_supplier_category = SupplierCategory.objects.get(
                    id=supplierCategory['id'])
                new_supplier_categories.append(new_supplier_category)
            supplier.supplierCategories.set(new_supplier_categories)
            supplier.save()
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'supplier categories was changed',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide supplier categories'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def update_company_name(self, request, pk=None):
        if request.data:
            supplier = Supplier.objects.get(id=pk)
            supplier.companyName = request.data['companyName']
            supplier.save()
            supplierSerializer = SupplierSerializer(supplier, many=False)
            response = {'message': 'supplier compnay name was changed',
                        'result': supplierSerializer.data}
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'you need to provide supplier compnay name'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ConsumerClientViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConsumerClientReadSerializer
        return ConsumerClientSerializer
    queryset = ConsumerClient.objects.all()
    authentication_classes = (TokenAuthentication,)

    @action(detail=False, methods=['GET'])
    def by_user(self, request, pk=None):
        client = ConsumerClient.objects.by_user(user=request.user)
        serializer = ConsumerClientReadSerializer(client, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def by_user_id(self, request, pk=None):
        user_id = request.data.get('user', None)
        user = User.objects.get(id=user_id)
        client = ConsumerClient.objects.by_user(user=user)
        serializer = ConsumerClientReadSerializer(client, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BusinessClientViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BusinessClientReadSerializer
        return BusinessClientSerializer
    queryset = BusinessClient.objects.all()
    authentication_classes = (TokenAuthentication,)

class ContactViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ContactReadSerializer
        return ContactSerializer
    queryset = Contact.objects.all()
    authentication_classes = (TokenAuthentication,)

class SupplierContactViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SupplierContactReadSerializer
        return SupplierContactSerializer
    queryset = SupplierContact.objects.all()
    authentication_classes = (TokenAuthentication,)

class BusinessClientContactViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BusinessClientContactReadSerializer
        return BusinessClientContactSerializer
    queryset = BusinessClientContact.objects.all()
    authentication_classes = (TokenAuthentication,)
    filter_class = BusinessClientContactFilter

    @action(detail=False, methods=['GET'])
    def by_user(self, request):
        contact = BusinessClientContact.objects.by_user(user=request.user)
        serializer = ContactReadSerializer(contact, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def by_user_id(self, request):
        user_id = request.data.get('user', None)
        user = User.objects.get(id=user_id)
        contact = BusinessClientContact.objects.by_user(user=user)
        serializer = ContactReadSerializer(contact, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    """
    API endpoint that lists all clients (Business & Consumer) clients.
    """

    def list(self, request):
        queryset = list(itertools.chain(ConsumerClient.objects.all(), BusinessClient.objects.all()))
        serializer = AllClientSerializer(queryset, many=True)
        return Response(serializer.data)

class TestView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    # permission_classes = []
    def post(self, request):
        test_header = request.headers
        print("tenant ", test_header)
        response = requests.get("https://joole-api.herokuapp.com/cms/mainTabItem/",
                                headers=test_header)
        print("RES", response.reason)
        if response.status_code != 200:
            return Response({"FAIL": response})
        accounts = response.json()
        return Response({"message": "Got some data!", "data": accounts})

class TestAccountViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TestAccountSerializer
        return TestAccountSerializer
    queryset = TestAccount.objects.all()
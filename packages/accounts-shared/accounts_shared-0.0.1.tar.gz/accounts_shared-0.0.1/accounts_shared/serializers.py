from rest_framework import serializers
from .models import (CompanyLocation, Supplier,
                     SupplierCategory, BusinessClient, ConsumerClient,
                     Address, Country, BusinessAccount, Account,
                     City, ShippingAddress, BillingAddress,
                     Contact, Company, CertificationEntity, Lead,
                     SupplierContact, BusinessClientContact, TestAccount,
                     )
from .enums import AccountTypeChoices
from team_common.serializers import TitleSerializer


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        if extension is None:
            return 'jpg'

        return extension


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'firstName', 'lastName', 'email', 'phoneNumber',
                  'description', 'createdOn', 'isActive', 'profilePicture', 'title']


class BusinessClientContactSerializer(ContactSerializer):

    class Meta:
        model = BusinessClientContact
        fields = ContactSerializer.Meta.fields + ['account']


class SupplierContactSerializer(ContactSerializer):

    class Meta:
        model = SupplierContact
        fields = ContactSerializer.Meta.fields + ['account']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['name', 'website', 'phoneNumber', 'email', 'id', 'profilePicture',
                  'businessClient']


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['name', 'code', 'id']


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['name', 'code', 'id']


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'addressLine1', 'addressLine2',
                  'region', 'city', 'postalCode', 'country', 'account', 'name']


class AddressReadSerializer(AddressSerializer):
    country = CountrySerializer(many=False)
    city = CitySerializer(many=False)

    class Meta:
        model = Address
        fields = AddressSerializer.Meta.fields + ['value']


class CompanyReadSerializer(CompanySerializer):
    addresses = AddressReadSerializer(many=True)

    class Meta:
        model = Company
        fields = CompanySerializer.Meta.fields + ['employees', 'addresses']


class AccountSerializer(serializers.ModelSerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Account
        fields = ['id', 'profilePicture', 'createdBy', 'createdOn',
                  'balance', 'notes', 'accountType', 'isActive', 'addresses', 'name']


class AccountReadSerializer(AccountSerializer):
    addresses = AddressReadSerializer(many=True)

    class Meta:
        model = Account
        fields = AccountSerializer.Meta.fields


class BusinessAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessAccount
        fields = ['id', 'email', 'phoneNumber', 'name', 'website', 'belongsTo']


class CertificationEntitySerializer(serializers.ModelSerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = CertificationEntity
        fields = ['id', 'email', 'phoneNumber', 'name', 'website', 'code',
                  'accountType', 'profilePicture', 'description', 'balance', 'isActive']


class ShippingAddressSerializer(AddressSerializer):

    class Meta:
        model = ShippingAddress
        fields = AddressSerializer.Meta.fields


class ShippingAddressReadSerializer(AddressSerializer):
    country = CountrySerializer(many=False)
    city = CitySerializer(many=False)
    addressType = serializers.CharField(source='get_addressType_display')

    class Meta:
        model = ShippingAddress
        fields = AddressSerializer.Meta.fields + ['addressType']


class BillingAddressSerializer(AddressSerializer):
    country = CountrySerializer(many=False)

    class Meta:
        model = BillingAddress
        fields = AddressSerializer.Meta.fields


class BillingAddressReadSerializer(AddressSerializer):
    country = CountrySerializer(many=False)
    city = CitySerializer(many=False)

    class Meta:
        model = BillingAddress
        fields = AddressSerializer.Meta.fields


class SupplierCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierCategory
        fields = ['id', 'name']


class SupplierSerializer(serializers.ModelSerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'balance', 'email', 'supplierCategories', 'profilePicture',
                  'phoneNumber', 'description', 'notes', 'website', 'accountType',
                  'belongsTo', 'payableAccount', 'creditLimit']


class SupplierReadSerializer(SupplierSerializer):
    addresses = AddressReadSerializer(many=True)
    supplierCategories = SupplierCategorySerializer(many=True)
    contacts = SupplierContactSerializer(many=True)

    class Meta:
        model = Supplier
        fields = SupplierSerializer.Meta.fields + ['addresses', 'contacts']


class CertificationEntityReadSerializer(CertificationEntitySerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = CertificationEntity
        fields = CertificationEntitySerializer.Meta.fields + ['addresses']


class ConsumerClientSerializer(serializers.ModelSerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = ConsumerClient
        fields = ['id', 'profilePicture', 'createdBy', 'createdOn',
                  'isActive', 'balance', 'notes', 'name', 'email',
                  'phoneNumber', 'age', 'sex', 'accountType',
                  'belongsTo', 'receivableAccount', 'creditLimit', 'clientCategories', 'dateOfBirth']


class BusinessClientSerializer(serializers.ModelSerializer):
    profilePicture = Base64ImageField(
        max_length=None, use_url=True, required=False
    )

    class Meta:
        model = BusinessClient
        fields = ['id', 'profilePicture', 'createdBy', 'createdOn',
                  'isActive', 'balance', 'notes', 'name', 'email',
                  'phoneNumber', 'bio', 'website', 'accountType',
                  'belongsTo', 'receivableAccount', 'creditLimit', 'clientCategories']


class BusinessClientContactReadSerializer(BusinessClientContactSerializer):
    account = BusinessClientSerializer(many=False)
    title = TitleSerializer(many=False)

    class Meta:
        model = BusinessClientContact
        fields = BusinessClientContactSerializer.Meta.fields + ['fullName']


class SupplierContactReadSerializer(SupplierContactSerializer):
    account = SupplierReadSerializer(many=False)
    title = TitleSerializer(many=False)

    class Meta:
        model = SupplierContact
        fields = SupplierContactSerializer.Meta.fields + ['fullName']


class ContactReadSerializer(ContactSerializer):
    title = TitleSerializer(many=False)

    class Meta:
        model = Contact
        fields = ContactSerializer.Meta.fields + ['fullName']


class BusinessClientReadSerializer(BusinessClientSerializer):
    addresses = AddressReadSerializer(many=True)
    contacts = BusinessClientContactReadSerializer(many=True)

    class Meta:
        model = BusinessClient
        fields = BusinessClientSerializer.Meta.fields + \
            ['addresses', 'contacts']


class ConsumerClientReadSerializer(ConsumerClientSerializer):
    addresses = AddressReadSerializer(many=True)

    class Meta:
        model = ConsumerClient
        fields = ConsumerClientSerializer.Meta.fields + ['addresses']


class AllClientSerializer(serializers.Serializer):
    """ Serializer that renders each client with its own specific serializer """

    @classmethod
    def get_serializer(cls, model):
        if model == ConsumerClient:
            return ConsumerClientReadSerializer
        elif model == BusinessClient:
            return BusinessClientReadSerializer
        elif model == Account:
            return AccountReadSerializer

    def to_representation(self, instance):
        serializer = self.get_serializer(instance.__class__)
        return serializer(instance, context=self.context).data


class SpecificAccountByAccountTypeSerializer(serializers.Serializer):
    """ Serializer that renders each account with its own specific serializer """

    def to_representation(self, value):
        if value.accountType == AccountTypeChoices.BUSINESSCLIENT:
            account = BusinessClient.objects.get(id=value.id)
            serializer = BusinessClientReadSerializer(
                account, context=self.context)

        elif value.accountType == AccountTypeChoices.CONSUMERCLIENT:
            account = ConsumerClient.objects.get(id=value.id)
            serializer = ConsumerClientReadSerializer(
                account, context=self.context)
        elif value.accountType == AccountTypeChoices.COMPANY:
            account = Company.objects.get(id=value.id)
            serializer = CompanyReadSerializer(account, context=self.context)
        elif value.accountType == AccountTypeChoices.SUPPLIER:
            account = Supplier.objects.get(id=value.id)
            serializer = SupplierReadSerializer(account, context=self.context)
        else:
            raise Exception('Unexpected type of account object')

        return serializer.data


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lead
        fields = ['id', 'createdBy', 'createdOn',
                  'email', 'phoneNumber', 'status', 'source', 'website',
                  'description', 'assignedTo', 'opportunityAmount',
                  'account', 'firstName', 'lastName', 'accountType', 'isActive', 'addresses']


class LeadReadSerializer(LeadSerializer):
    addresses = AddressReadSerializer(many=True)

    class Meta:
        model = Lead
        fields = LeadSerializer.Meta.fields


class CompanyLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyLocation
        fields = ['id', 'address', 'title', 'email', 'phoneNumber', 'image']


class CompanyLocationReadSerializer(CompanyLocationSerializer):
    address = AddressReadSerializer(many=False)

    class Meta:
        model = CompanyLocation
        fields = CompanyLocationSerializer.Meta.fields


# class ResellerStoreSerializer(CompanyLocationSerializer):

#     class Meta:
#         model = CompanyLocation
#         fields = CompanyLocationSerializer.Meta.fields + ['businessClient']


# class ResellerStoreReadSerializer(ResellerStoreSerializer):
#     address = AddressReadSerializer(many=False)

#     class Meta:
#         model = CompanyLocation
#         fields = ResellerStoreSerializer.Meta.fields

class TestAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAccount
        fields = ['id', 'createdOn',
                  'balance', 'notes', 'isActive', 'name']

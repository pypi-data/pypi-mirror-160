from django.db import models
from .enums import SexChoice, AddressTypeChoices, AccountTypeChoices
from .choices import (STATUS_CHOICE, LEAD_STATUS, LEAD_SOURCE)
from .managers import (ContactManager, ConsumerClientManager)

class City(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    code = models.CharField(blank=True, max_length=3, null=True)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return self.name

class Country(models.Model):
    name = models.CharField(max_length=60, null=True, blank=True)
    code = models.CharField(blank=True, max_length=3, null=True)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

    def __str__(self):
        return self.name + ' (' + self.code + ')'

class TestAccount(models.Model):
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, max_digits=10, null=True, default=0)
    notes = models.TextField(blank=True, max_length=1000, default='')
    name = models.CharField(blank=False, max_length=60, null=True)

    class Meta:
        verbose_name = 'Test Account'
        verbose_name_plural = 'Test Accounts'

    def __str__(self):
        return self.name

class Account(models.Model):
    profilePicture = models.ImageField(upload_to='accounts-profile-pictures',
                                       blank=True, default="defaultImage.jpg", null=True)
    createdBy = models.ForeignKey('team_common.User', on_delete=models.SET_NULL, null=True, related_name="accountsCreatedByMe")
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    balance = models.DecimalField(decimal_places=2, max_digits=10, null=True, default=0)
    notes = models.TextField(blank=True, max_length=1000, default='')
    accountType = models.PositiveSmallIntegerField(choices=AccountTypeChoices.choices, null=True, blank=True)
    name = models.CharField(blank=False, max_length=60, null=True)
    customerId = models.CharField(blank=True, max_length=200, null=True)
    # refactor... add phonenumber here.

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.name

class Address(models.Model):
    name = models.CharField(blank=False, max_length=60, null=True)
    addressLine1 = models.CharField(blank=False, max_length=60)
    addressLine2 = models.CharField(blank=True, max_length=60)
    region = models.CharField("State / Province / Region", blank=False, max_length=60)
    postalCode = models.CharField("ZIP / Postal code", max_length=12)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)
    country = models.ForeignKey(Country, blank=True, null=True, on_delete=models.SET_NULL)
    account = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL,
                                related_name="addresses")

    @property
    def value(self):
        if self.addressLine2 is None or not self.addressLine2:
            return self.addressLine1 + ', ' + self.city.name + ', ' + self.region + ', ' + self.country.name + ', ' + self.postalCode
        else:
            return self.addressLine1 + ', ' + self.addressLine2 + ', ' + self.city.name + ', ' + self.region + ', ' + self.country.name + ', ' + self.postalCode

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        if self.addressLine2 is None:
            return self.addressLine1 + ', ' + self.city.name + ', ' + self.region + ', ' + self.country.name + ', ' + self.postalCode
        else:
            return self.addressLine1 + ', ' + self.addressLine2 + ', ' + self.city.name + ', ' + self.region + ', ' + self.country.name + ', ' + self.postalCode


class ShippingAddress(Address):
    addressType = models.CharField(max_length=10, choices=AddressTypeChoices.choices(),
                                   default=AddressTypeChoices.SHIPPING)

    class Meta:
        verbose_name = 'Shipping Address'
        verbose_name_plural = 'Shipping Addresses'

    def __str__(self):
        return "Shipping Address " + str(self.id)


class BillingAddress(Address):
    addressType = models.CharField(max_length=10, choices=AddressTypeChoices.choices(),
                                   default=AddressTypeChoices.BILLING)

    class Meta:
        verbose_name = 'Billing Address'
        verbose_name_plural = 'Billing Addresses'

    def __str__(self):
        return "Billing Address " + str(self.id)


class Company(Account):
    email = models.EmailField(blank=True, max_length=254, unique=True, null=True)
    phoneNumber = models.CharField(blank=True, max_length=20, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    plan = models.ForeignKey('plans_shared.Plan', null=True, blank=True, related_name="companies",
                             on_delete=models.SET_NULL)
    businessClient = models.OneToOneField('accounts_shared.BusinessClient', related_name='company',
                                on_delete=models.SET_NULL, blank=True, null=True)
    
    # def get_company(request):
    #     company = request.user.employee.company
    #     return company

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'

    def __str__(self):
        return "Company " + str(self.id)

class ClientCategory(models.Model):
    name = models.CharField(blank=False, max_length=60, null=False)

    class Meta:
        verbose_name = 'Client Category'
        verbose_name_plural = 'Client Categories'

    def __str__(self):
        return self.name


class BusinessAccount(Account):
    email = models.EmailField(blank=False, max_length=254)
    phoneNumber = models.CharField(blank=False, max_length=20)
    website = models.URLField(max_length=500, blank=True, null=True)
    belongsTo = models.ForeignKey(Company,related_name='businessAccounts',
                                on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Business Account'
        verbose_name_plural = 'Business Accounts'

    def __str__(self):
        return self.name


class Contact(models.Model):
    objects = ContactManager()
    DEFAULT_PICTURE = "../media/defaultImage.jpg"
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    profilePicture = models.ImageField(upload_to='contact-profile-pictures',
                                       blank=True, default=DEFAULT_PICTURE, null=True)
    title = models.ForeignKey(
        'team_common.Title', on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def fullName(self):
        return self.firstName + ' ' + self.lastName

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.firstName + self.lastName


class SupplierCategory(models.Model):
    name = models.CharField(blank=False, max_length=60)

    class Meta:
        verbose_name = 'Supplier Category'
        verbose_name_plural = 'Supplier Categories'

    def __str__(self):
        return self.name


class Supplier(BusinessAccount):
    description = models.TextField(blank=True, max_length=1000, default='')
    supplierCategories = models.ManyToManyField(SupplierCategory, related_name="suppliers", blank=True)
    payableAccount = models.ForeignKey('accounting_shared.ChartAccount', null=True, blank=True, on_delete=models.SET_NULL)
    creditLimit = models.OneToOneField('accounting_shared.CreditLimit', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="supplier")

    class Meta:
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'

    def __str__(self):
        return self.name


class CertificationEntity(BusinessAccount):
    code = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=True, max_length=1000, default='')

    class Meta:
        verbose_name = 'CertificationEntity'
        verbose_name_plural = 'CertificationEntities'

    def __str__(self):
        return self.name

class BusinessClient(BusinessAccount):
    bio = models.TextField(blank=True, max_length=1000, default='')
    isReseller = models.BooleanField(default=False)
    receivableAccount = models.ForeignKey('accounting_shared.ChartAccount', null=True, blank=True, on_delete=models.SET_NULL)
    creditLimit = models.OneToOneField('accounting_shared.CreditLimit', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="businessClient")
    clientCategories = models.ManyToManyField(ClientCategory, related_name="businessClients", blank=True)

    class Meta:
        verbose_name = 'Business Client'
        verbose_name_plural = 'Business Clients'

class SupplierContact(Contact):
    account = models.ForeignKey(Supplier, related_name='contacts',
                                on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Supplier Contact'
        verbose_name_plural = 'Supplier Contacts'

    def __str__(self):
        return "Suipplier Contact " + str(self.id)


class BusinessClientContact(Contact):
    account = models.ForeignKey(BusinessClient, related_name='contacts',
                                on_delete=models.SET_NULL, blank=True, null=True)
    user = models.OneToOneField('team_common.User', related_name='contact',
                                on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Business Client Contact'
        verbose_name_plural = 'Business Client Contacts'

    def __str__(self):
        if self.firstName and self.lastName:
            return self.firstName + " " + self.lastName
        else:
            return "Business Client Contact " + str(self.id)


class ConsumerClient(Account):
    objects = ConsumerClientManager()
    email = models.EmailField(blank=False, max_length=254)
    phoneNumber = models.CharField(blank=False, max_length=20)
    age = models.PositiveIntegerField(default=0)
    dateOfBirth = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SexChoice.choices())
    user = models.OneToOneField('team_common.User', on_delete=models.SET_NULL, null=True, blank=True, related_name="account")
    belongsTo = models.ForeignKey(Company,related_name='consumerClients',
                                on_delete=models.SET_NULL, blank=True, null=True)
    receivableAccount = models.ForeignKey('accounting_shared.ChartAccount', null=True, blank=True, on_delete=models.SET_NULL)
    creditLimit = models.OneToOneField('accounting_shared.CreditLimit', null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name="consumerClient")
    clientCategories = models.ManyToManyField(ClientCategory, related_name="consumerClients", blank=True)

    class Meta:
        verbose_name = 'Consumer Client'
        verbose_name_plural = 'Consumer Clients'
        unique_together = ('belongsTo', 'email')


class Lead(models.Model):
    firstName = models.CharField(null=False, blank=False, max_length=50)
    lastName = models.CharField(null=False, blank=False, max_length=50)
    email = models.EmailField(null=False, blank=False)
    phoneNumber = models.CharField(null=True, blank=True, max_length=50)
    status = models.CharField(max_length=255, blank=True, null=True, choices=LEAD_STATUS
                              )
    source = models.CharField(max_length=255, blank=True, null=True, choices=LEAD_SOURCE)
    addresses = models.ManyToManyField(Address, related_name="leads")
    website = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assignedTo = models.ManyToManyField('team.Employee', related_name="myLeads")
    opportunityAmount = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True
                                            )
    createdBy = models.ForeignKey('team.Employee', on_delete=models.SET_NULL, null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    isActive = models.BooleanField(default=False)
    # enquery_type = models.CharField(max_length=255, blank=True, null=True)
    # tags = models.ManyToManyField(Tags, blank=True)
    # contacts = models.ManyToManyField(Contact, related_name="contacts")
    # created_from_site = models.BooleanField(default=False)
    # teams = models.ManyToManyField(Teams, related_name="lead_teams")
    # account = models.ForeignKey(
    #     Account, on_delete=models.SET_NULL, null=True, blank=True
    # )

    class Meta:
        ordering = ["-createdOn"]
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return self.email

# TODO: add hours of CompanyLocation

class CompanyLocation(models.Model):
    DEFAULT_PICTURE = "../media/defaultImage.jpg"

    email = models.EmailField(blank=False, max_length=254)
    phoneNumber = models.CharField(blank=False, max_length=20)
    title = models.CharField(blank=False, null=False, max_length=200)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='company-location-pictures',
                              blank=True, default=DEFAULT_PICTURE, null=True)

    class Meta:
        verbose_name = 'Company Location'
        verbose_name_plural = 'Company Locations'

    def __str__(self):
        return self.title

class Store(models.Model):
    DEFAULT_PICTURE = "../media/defaultImage.jpg"

    email = models.EmailField(blank=False, max_length=254)
    phoneNumber = models.CharField(blank=False, max_length=20)
    title = models.CharField(blank=False, null=False, max_length=200)
    # address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='store-pictures',
                              blank=True, default=DEFAULT_PICTURE, null=True)

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

    def __str__(self):
        return self.title






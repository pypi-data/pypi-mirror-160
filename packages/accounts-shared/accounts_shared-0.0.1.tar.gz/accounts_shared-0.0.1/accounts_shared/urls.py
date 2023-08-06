from django.urls import include, path
from rest_framework import routers

from accounts_shared.reports.accounts_reports import ConsumerClientsByAgeView
from accounts_shared.reports.business_clients_reports import BusinessClientsByCityView
from .views import (AddressViewSet, SupplierCategoryViewSet,
                    SupplierViewSet, CountryViewSet, BillingAddressViewSet,
                    BusinessClientViewSet, ConsumerClientViewSet, AccountViewSet,
                    ContactViewSet, CompanyViewSet, ClientViewSet,
                    CertificationEntityViewSet, MyCompanyView,
                    CityViewSet, 
                    ShippingAddressesByAccountList,
                    AddressesByAccountList,
                    ShippingAddressViewSet,
                    BookAnAppointmentSearchCompanyLocationsView,
                    BusinessClientContactViewSet,
                    SupplierContactViewSet,
                    CompanyLocationViewSet, TestAccountViewSet, TestView,
                    # ResllerStoreViewSet,
                    )
router = routers.DefaultRouter()
router.register('address', AddressViewSet)
router.register('supplier', SupplierViewSet)
router.register('supplier-category', SupplierCategoryViewSet)
router.register('countries', CountryViewSet)
router.register('billingAddress', BillingAddressViewSet)
router.register('consumerClient', ConsumerClientViewSet)
router.register('businessClient', BusinessClientViewSet)
router.register('account', AccountViewSet)
router.register('contact', ContactViewSet)
router.register('businessClientContact', BusinessClientContactViewSet)
router.register('supplierContact', SupplierContactViewSet)
router.register('country', CountryViewSet)
router.register('city', CityViewSet)
router.register('companyLocation', CompanyLocationViewSet)
# router.register('resllerStore', ResllerStoreViewSet)
router.register('company', CompanyViewSet)
router.register('client', ClientViewSet, basename='client')
router.register('certificationEntity', CertificationEntityViewSet)
router.register('shippingAddress', ShippingAddressViewSet)
router.register('testAccount', TestAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('myCompany/', MyCompanyView.as_view()),
    path('shipping_addresses_by_account/', ShippingAddressesByAccountList.as_view()),
    path('addresses_by_account/', AddressesByAccountList.as_view()),
    path('book_an_appointment_search_company_locations/', BookAnAppointmentSearchCompanyLocationsView.as_view()),
    path('report_consumer_clients_by_age/', ConsumerClientsByAgeView.as_view()),
    path('report_business_clients_by_city/', BusinessClientsByCityView.as_view()),
    path('test/', TestView.as_view()),

]

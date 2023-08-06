from enum import Enum
from django.db import models
 

class SexChoice(Enum):
    MALE = "Male"
    FEMALE = "Female"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class AddressTypeChoices(Enum):
    BILLING = "Billing"
    SHIPPING = "Shipping"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class AccountTypeChoices(models.IntegerChoices):
    CONSUMERCLIENT = 0
    BUSINESSCLIENT = 1
    SUPPLIER = 2
    COMPANY = 3
    CERTIFICATIONENTTIY = 4
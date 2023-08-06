from django.db import models

# from users.enums import UserTypeChoices


class ContactManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def by_user(self, user):
        user_type = user.userType
        # if user_type == UserTypeChoices.EMPLOYEE or user_type == UserTypeChoices.RETAILER:
        #     return super().get_queryset().get(
        #         user=user)
        # else:
        #     raise Exception("This user type does not have a Contact")


class ConsumerClientManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def by_user(self, user):
        user_type = user.userType
        # if user_type == UserTypeChoices.CONSUMER:
        #     return super().get_queryset().get(
        #         user=user)
        # else:
        #     raise Exception("User is not a ConsumerClient")

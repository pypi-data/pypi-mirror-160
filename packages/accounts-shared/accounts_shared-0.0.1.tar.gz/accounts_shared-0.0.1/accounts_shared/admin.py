from django.contrib import admin
from django.apps import apps

app = apps.get_app_config('accounts_shared')
admin.site.register(app.get_models())

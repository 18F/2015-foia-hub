from django.contrib import admin
from foia_hub.models import *


class GenericAdmin(admin.ModelAdmin):
    pass

admin.site.register(Office, GenericAdmin)
admin.site.register(Agency, GenericAdmin)
#admin.site.register(Person, GenericAdmin)

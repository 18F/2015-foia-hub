from django.contrib import admin
from foia_hub.models import Office, Agency


class GenericAdmin(admin.ModelAdmin):
    pass

admin.site.register(Office, GenericAdmin)
admin.site.register(Agency, GenericAdmin)

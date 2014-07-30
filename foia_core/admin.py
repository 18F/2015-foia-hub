from django.contrib import admin
from foia_core.models import Department, Agency, FOIAContact


class GenericAdmin(admin.ModelAdmin):
    pass


admin.site.register(Department, GenericAdmin)
admin.site.register(Agency, GenericAdmin)
admin.site.register(FOIAContact, GenericAdmin)

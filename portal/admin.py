from django.contrib import admin
from portal.models import *
# Register your models here.

class OrganisationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'updated')

admin.site.register(OrganisationType, OrganisationTypeAdmin)

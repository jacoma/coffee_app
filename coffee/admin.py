from django.contrib import admin
from .models import *
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin

class coffeeResource(resources.ModelResource):

    class Meta:
        model = dim_coffee

class coffeeAdmin(ImportExportActionModelAdmin):
    resource_class = coffeeResource

# Register your models here.
admin.site.register(ratings)
admin.site.register(dim_roaster)
admin.site.register(dim_notes)
admin.site.register(dim_varietal)
admin.site.register(countries)
admin.site.register(dim_coffee, coffeeAdmin)
from django.contrib import admin

from . import models


class OperatorAdmin(admin.ModelAdmin):
    list_display = ['operator_name', 'network']


admin.site.register(models.Location)
admin.site.register(models.Permission)
admin.site.register(models.Operator, OperatorAdmin)
admin.site.register(models.RawRecord)

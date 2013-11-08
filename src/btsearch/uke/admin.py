from django.contrib import admin

from . import models


class OperatorAdmin(admin.ModelAdmin):
    list_display = ['operator_name', 'network']


admin.site.register(models.Operator, OperatorAdmin)

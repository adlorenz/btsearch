from django.contrib import admin

from . import models


class UkeOperatorAdmin(admin.ModelAdmin):
    list_display = ['operator_name', 'network']


admin.site.register(models.UkeOperator, UkeOperatorAdmin)

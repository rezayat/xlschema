from django.contrib import admin

from . import models

register = get_register(models, admin)


@register
class ${classname}Admin(admin.ModelAdmin):
    list_display = ${tuple(list_display)}
    search_fields = ${[fieldname for fieldname in search_fields]}
    list_filter = ${tuple(list_display)}

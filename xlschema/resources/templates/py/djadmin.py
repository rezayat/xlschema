from django.contrib import admin

# Register your models here.
from .models import ${data.imports}

% for model in data.schema.models:
class ${model.classname}Admin(admin.ModelAdmin):
    list_display = ${model.fieldnames}
    list_filter = ${model.enum_fieldnames}
    % if model.has_sk:
    search_fields = ['${model.sk_field.name}']
    % endif
    fieldsets = [
        (None, {'fields': ${model.noncategory_admin_fieldnames}}),
    % if model.categories:
        % for category in model.categories:
        ('${category}', {'fields': ${model.fieldnames_for_category(category)}}),
        % endfor
    % endif
    ]

admin.site.register(${model.classname}, ${model.classname}Admin)

% endfor

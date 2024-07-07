
from tastypie.resources import ModelResource
## from tastypie.authorization import Authorization
from .models import ${classname}

class ${classname}Resource(ModelResource):
    class Meta:
        queryset = ${classname}.objects.all()
        resource_name = ${name}
        ## authorization = Authorization()

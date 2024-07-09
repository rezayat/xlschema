
from tastypie.resources import ModelResource
## from tastypie.authorization import Authorization
from .models import ${model.classname}

class ${model.classname}Resource(ModelResource):
    class Meta:
        queryset = ${model.classname}.objects.all()
        resource_name = ${model.name}
        ## authorization = Authorization()

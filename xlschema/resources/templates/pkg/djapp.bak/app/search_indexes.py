from haystack import indexes
from .models import ${classname}


class ${classname}Index(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    % for fieldname in search_fields:
    ${fieldname} = indexes.CharField(model_attr='${fieldname}')
    % endfor

    def get_model(self):
        return ${classname}

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

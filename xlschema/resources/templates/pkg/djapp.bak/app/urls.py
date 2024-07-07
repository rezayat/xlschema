from django.conf.urls import url, patterns
## from django.views.generic import TemplateView

from .views import (
    # ${classname}IndexView,
    ${classname}ListView,
    ${classname}CreateView,
    ${classname}DetailView,
    ${classname}UpdateView,
    ${classname}DeleteView,
)

from .api import ${classname}Resource

${name}_resource = ${classname}Resource()

# urlpatterns = patterns('${app}.views',

# )

urlpatterns = patterns('',
    # url(r'^$', ${classname}IndexView.as_view(), name='${url_index}'),
    # url(r'^list/$', ${classname}ListView.as_view(), name='${url_list}'),
    url(r'^$', ${classname}ListView.as_view(), name='${url_list}'),
    url(r'^(?P<pk>\d+)/$', ${classname}DetailView.as_view(), name='${url_detail}'),
    url(r'^(?P<pk>\d+)/update/$', ${classname}UpdateView.as_view(), name='${url_update}'),
    url(r'^(?P<pk>\d+)/delete/$', ${classname}DeleteView.as_view(), name='${url_delete}'),
    url(r'^create/$', ${classname}CreateView.as_view(), name='${url_create}'),
    
    # restful api
    url(r'^api/', include(entry_resource.urls), name='${name}-api'),
)

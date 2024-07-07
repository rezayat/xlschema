from django.core.urlresolvers import reverse_lazy
# from django.shortcuts import render_to_response
# from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views import generic
from django.contrib.auth.decorators import login_required

from .models import ${classname}
from .forms import ${classname}Form


@login_required
class ${classname}IndexView(generic.TemplateView):
    template_name = '${path}/${name}_index.html'


@login_required
class ${classname}ListView(generic.ListView):
    template_name = '${path}/${name}_list.html'
    model = ${classname}
    context_object_name = '${plural}'


@login_required
class ${classname}DeleteView(generic.DeleteView):
    template_name = '${path}/${name}_delete.html'
    model = ${classname}
    context_object_name = '${name}'
    success_url = reverse_lazy('${url_list}')


@login_required
class ${classname}DetailView(generic.DetailView):
    template_name = '${path}/${name}_detail.html'
    model = ${classname}

    def get_context_data(self, **kwargs):
        context = super(${classname}DetailView, self).get_context_data(**kwargs)
        form = ${classname}Form(instance=context['object'])
        form.set_readonly()
        form.helper.inputs = []
        context['form'] = form
        return context


@login_required
class ${classname}CreateView(generic.CreateView):
    template_name = '${path}/${name}_create.html'
    form_class = ${classname}Form
    model = ${classname}
    success_url = reverse_lazy('${url_list}')


@login_required
class ${classname}UpdateView(generic.UpdateView):
    template_name = '${path}/${name}_update.html'
    form_class = ${classname}Form
    model = ${classname}
    context_object_name = '${name}'
    success_url = reverse_lazy('${url_list}')

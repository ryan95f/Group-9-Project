from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse

from module.models import Module
from module.forms import ModuleForm
from latexbook.models import Book


class ModuleIndexView(ListView):
    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.all()


class ModuleDashboardView(TemplateView):
    template_name = 'module/module_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleDashboardView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm
        return context


class ModuleDetailsView(TemplateView):
    template_name = 'module/module_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleDetailsView, self).get_context_data(**kwargs)
        context['module'] = get_object_or_404(Module, pk=kwargs['pk'])
        return context

             
class AjaxableResponseMixin(object):
    
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'module_code': self.object.code,
                'module_title': self.object.title,
                'module_year': self.object.year,
            }
            return JsonResponse(data)
        else:
            return response

class NewModule(AjaxableResponseMixin, CreateView):
    model = Module
    template_name = 'module/module_dashboard.html'
    fields = ['code','title','year']

    def get_context_data(self, **kwargs):
        context = super(NewModule, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm
        return context


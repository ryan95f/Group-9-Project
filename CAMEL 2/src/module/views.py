from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


from module.forms import ModuleForm
from module.models import Module


class ModuleIndexView(ListView):
    """View for displaying all modules in CAMEL"""

    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        """Return context data for displaying the list of objects.."""
        return Module.objects.all()


class ModuleDashboardView(TemplateView):
    """View for Module Dashboard - requires login
    see urls.py"""

    template_name = 'module/module_dashboard.html'

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects.."""
        context = super(ModuleDashboardView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm()
        return context


class ModuleDetailsView(TemplateView):
    """View for getting module specifics"""

    template_name = 'module/module_detail.html'

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects.."""
        context = super(ModuleDetailsView, self).get_context_data(**kwargs)

        context['module'] = get_object_or_404(Module, pk=kwargs['pk'])
        context['learningmaterials'] = {}

        for learningmaterial in context['module'].learningmaterial_set.all():
            material = learningmaterial.material_content_object
            context['learningmaterials'].setdefault(material.__class__.__name__, []).append(material)

        return context


class AjaxableResponseMixin(object):
    """Ajax and non-ajax response class"""

    def form_invalid(self, form):
        """Valid form method concerning
         module for ajax and non-ajax post requests"""
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        """Valid form method for new module post request"""
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
    """Add new module View, utilises AjaxableResponseMixin Object"""

    model = Module
    template_name = 'module/module_dashboard.html'
    fields = ['code', 'title', 'year']

    def get_context_data(self, **kwargs):
        """Aquire context data for template"""
        context = super(NewModule, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm
        return context

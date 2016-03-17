from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import generic

from module.forms import ModuleForm
from module.models import Module


class ModuleIndexView(generic.ListView):
    """Blah, blah, blah."""

    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        """Return context data for displaying the list of objects.."""
        return Module.objects.all()


class ModuleDashboardView(generic.base.TemplateView):
    """Blah, blah, blah."""

    template_name = 'module/module_dashboard.html'

    def get_context_data(self, **kwargs):
        """Return context data for displaying the list of objects.."""
        context = super(ModuleDashboardView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm()
        return context


class ModuleDetailsView(generic.base.TemplateView):
    """Blah, blah, blah."""

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
    """Please add docstrings."""

    def form_invalid(self, form):
        """Please add docstrings."""
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        """Please add docstrings."""
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


class NewModule(AjaxableResponseMixin, generic.edit.CreateView):
    """Please add docstrings."""

    model = Module
    template_name = 'module/module_dashboard.html'
    fields = ['code', 'title', 'year']

    def get_context_data(self, **kwargs):
        """Please add docstrings."""
        context = super(NewModule, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm
        return context

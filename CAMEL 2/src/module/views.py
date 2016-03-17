from django.core.exceptions import ObjectDoesNotExist
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


def new_module(request):
    """Accept an AJAX request for creating a new module."""
    if(request.method == "POST"):
        try:
            module = Module.objects.get(pk=request.POST['module_code'])
            # return response that module alreay exists
            return JsonResponse({'key_exists': request.POST['module_code']})
        except ObjectDoesNotExist:
            module = Module(request.POST['module_code'], request.POST['module_year'], request.POST['module_title'])
            module.save()
            return JsonResponse(request.POST)

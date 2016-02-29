from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.http import JsonResponse, HttpResponse

from module.models import Module
from module.forms import ModuleForm
from latexbook.models import Book

class ModuleIndexView(generic.ListView):
    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.all()

class ModuleDashboardView(generic.base.TemplateView):
    template_name = 'module/module_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleDashboardView, self).get_context_data(**kwargs)
        context['module'] = Module.objects.all()
        context['form'] = ModuleForm()
        return context

class ModuleDetailsView(generic.base.TemplateView):
    template_name = 'module/module_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ModuleDetailsView, self).get_context_data(**kwargs)
        context['module'] = get_object_or_404(Module, pk=kwargs['pk'])
        return context


def new_module(request):
	if(request.method == "POST"):
		try:
			module = Module.objects.get(pk=request.POST['module_code'])
			# return response that module alreay exists
			return JsonResponse({'key_exists' : request.POST['module_code']})
		except ObjectDoesNotExist:
			module = Module(request.POST['module_code'], request.POST['module_year'], request.POST['module_title'])
			module.save()
			return JsonResponse(request.POST)
            
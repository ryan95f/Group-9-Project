from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.http import JsonResponse

from module.models import Module
from module.forms import ModuleForm
from latexbook.models import Book

class ModuleIndexView(generic.ListView):
    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.all()

class ModuleView(generic.View):
	template_name = 'module/module_dashboard.html'
	module = Module.objects.all()
	
	def get(self, request):
		return render(request, self.template_name, {'module' : self.module, 'form' : ModuleForm })


def new_module(request):
	if(request.method == "POST"):
		try:
			module = Module.objects.get(pk=request.POST['module_code'])
			# return response that module alreay exists
			return JsonResponse({'key_exists' : request.POST['module_code']})
		except ObjectDoesNotExist:
			# add new module
			module = Module(request.POST['module_code'], request.POST['module_year'], request.POST['module_title'])
			module.save()
			return JsonResponse(request.POST)

def module_detail(request, pk):
	module = get_object_or_404(Module, pk=pk)
	return render(request,'module/module_detail.html', {'module' : module })


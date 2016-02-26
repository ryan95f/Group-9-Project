from django.shortcuts import get_object_or_404, render
from django.views import generic

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
		return render(request, self.template_name, {'module' : self.module })


def module_detail(request, pk):
	module = get_object_or_404(Module, pk=pk)
	return render(request,'module/module_detail.html', {'module' : module })
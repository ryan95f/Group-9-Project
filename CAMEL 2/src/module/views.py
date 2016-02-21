from django.shortcuts import get_object_or_404, render
from django.views import generic

from module.models import Module
from latexbook.models import Book

class ModuleIndexView(generic.ListView):
    template_name = 'module/module_index.html'
    context_object_name = 'modules'

    def get_queryset(self):
        return Module.objects.all()

def module_detail(request, pk):
	module = get_object_or_404(Module, pk=pk)
	return render(request,'module/module_detail.html', {'module' : module })

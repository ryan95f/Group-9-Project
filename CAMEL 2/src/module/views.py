from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from latexbook.models import Module

def module_index(request):
	return render(request,'module/module_index.html', {'modules' : Module.objects.all()})

def module_detail(request, pk):
	module = get_object_or_404(Module, pk=pk)
	return render(request,'module/module_detail.html', {'module' : module })


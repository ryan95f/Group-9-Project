from django.shortcuts import render

from latexbook.models import Module

def module_index(request):
	return render(request,'module/module_index.html', {'modules' : Module.objects.all()})
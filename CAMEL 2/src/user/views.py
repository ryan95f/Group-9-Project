from django.shortcuts import render
from django.http import HttpResponseRedirect

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from user.models import CamelUser

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, request.POST)
		if form.is_valid():
			login(request, form.get_user())
			return render(request, 'user/userhome.html', {'pk': form.get_user().identifier })
		else:
			# user not found
			return HttpResponseRedirect('/user/login')
	else:
		form = AuthenticationForm(request)
		return render(request, "user/login.html", {"form": form })

@login_required
def userhome(request, pk):
	return render(request, 'user/userhome.html')

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


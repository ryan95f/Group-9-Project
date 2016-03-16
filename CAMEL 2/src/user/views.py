from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from user.models import CamelUser
from user.forms import SignUpForm


class UserView(FormView):
	'''A view form for adding new students to CAMEL '''

	template_name = 'user/sign_up.html'
	form_class = SignUpForm
	success_url = '/'

	def form_valid(self, form):
		clean_data = form.clean_form();
		new_user = CamelUser(
			identifier = clean_data['identifier'],
			first_name = clean_data['first_name'],
			last_name = clean_data['last_name'],
			is_an_student = True,
			is_an_lecturer = False,
			email = clean_data['email'],
			)
		new_user.set_password(clean_data['password1'])
		new_user.save()
		auth = authenticate(username=clean_data['identifier'], password=clean_data['password1'])
		login(self.request, auth)
		return super(UserView, self).form_valid(form)


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


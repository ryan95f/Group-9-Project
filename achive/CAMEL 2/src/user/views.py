from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import View
from django.views.generic.base import TemplateView

# auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

from user.models import CamelUser, CamelUserManager
from user.forms import SignUpForm


class UserView(FormView):
    """A view form for adding new students to CAMEL"""

    template_name = 'user/sign_up.html'
    form_class = SignUpForm
    user_identifier = None

    def form_valid(self, form):
        '''Method to add and login new students if valid form'''
        user_manager = CamelUserManager()
        user_manager.model = CamelUser

        clean_data = form.clean_form()
        self.user_identifier = clean_data['identifier']

        # checks to see that user identifier has not been registered
        try:
            user_manager.create_student(
                identifier=clean_data['identifier'], first_name=clean_data['first_name'],
                last_name=clean_data['last_name'], email=clean_data['email'], password=clean_data['password1']
            )
        except ValueError:
            # if it has been registered then redirect back to signup page
            return render(self.request, self.template_name, {
                'pk': self.user_identifier,
                'form': form,
                'error': str(self.user_identifier) + " has already been registered"
            })

        # login the student into camel
        auth = authenticate(username=clean_data['identifier'], password=clean_data['password1'])
        login(self.request, auth)
        return render(self.request, 'user/userhome.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        '''Method of aquire user identifier for template '''
        context = super(UserView, self).get_context_data(**kwargs)
        context['pk'] = self.user_identifier
        return context


class LoginView(FormView):
    '''A view to login users for CAMEL'''
    template_name = 'user/login.html'
    form_class = AuthenticationForm
    user_identifier = None

    def form_valid(self, form):
        '''Method that checks user to be logged in'''
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        self.user_identifier = username
        auth = authenticate(username=username, password=password)
        login(self.request, auth)
        return render(self.request, 'user/userhome.html', self.get_context_data())

    def get_context_data(self, **kwargs):
        '''Method of aquire user identifier for template '''
        context = super(LoginView, self).get_context_data(**kwargs)
        context['pk'] = self.user_identifier
        return context


class UserhomeView(TemplateView):
    '''View for the userhome page'''
    template_name = 'user/userhome.html'


class LogoutView(View):
    '''View for logging out users'''
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')

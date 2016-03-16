from django import forms
from user.models import CamelUser
from django.utils.datastructures import SortedDict

class SignUpForm(forms.Form):
	identifier = forms.CharField(label='Student Number', max_length=40, required=True)
	email = forms.EmailField(label='Student Email', required=True)
	first_name = forms.CharField(label='Student Name', max_length=40, required=True)
	last_name = forms.CharField(label='Student Surname', max_length=40, required=True)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

	class Meta:
		model = CamelUser
		fields = ()

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

	def clean_form(self):
		clean_identifer = self.cleaned_data['identifier']
		clean_email = self.cleaned_data['email']
		clean_fname = self.cleaned_data['first_name']
		clean_sname = self.cleaned_data['last_name']
		clean_pass1 = self.cleaned_data['password1']
		clean_pass2 = self.cleaned_data['password2']
		
		return {
			'identifier' : clean_identifer,
			'email' : clean_email,
			'first_name' : clean_fname,
			'last_name' : clean_sname,
			'password1' : clean_pass1,
			'password2' : clean_pass2,
		}

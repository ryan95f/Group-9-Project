from django import forms
from module.models import Module
from module.options import ACADEMIC_YEARS, MODULE_CODES

class ModuleForm(forms.Form):
	code = forms.ChoiceField(choices = MODULE_CODES,label="Code", widget=forms.Select(), required=True)
	year = forms.ChoiceField(choices = ACADEMIC_YEARS,label="Year", widget=forms.Select(), required=True)
	title = forms.CharField(max_length=64)
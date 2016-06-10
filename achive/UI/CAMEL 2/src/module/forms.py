from django import forms
from module.options import ACADEMIC_YEARS


class ModuleForm(forms.Form):
    """Form for inserting new modules"""
    code = forms.CharField(max_length=64)
    year = forms.ChoiceField(choices=ACADEMIC_YEARS, label="Year", widget=forms.Select(), required=True)
    title = forms.CharField(max_length=64)

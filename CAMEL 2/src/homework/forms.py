from django import forms
from homework.models import Answer

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['user', 'assignment']
        widgets = {
            'user': forms.HiddenInput(),
            'assignment': forms.HiddenInput(),
        }
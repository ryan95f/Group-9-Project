# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import modelformset_factory
from django.contrib.auth.models import User

from core.models import Module, BookNode, Label, Answer, SingleChoiceAnswer, Submission


# not sure where this came from
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        
# free-text answer form
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'user', 'text', 'is_readonly']
        widgets = {
            'question': forms.HiddenInput(),
            'user': forms.HiddenInput(),
            'is_readonly': forms.HiddenInput(),
            'text': forms.Textarea(
                attrs={'cols': '64', 'id': 'answer-text', 'required': True, 'placeholder': 'Type answer here...'}
            ),
        }

#  single-choice answer form (doesn't work)
# class SingleChoiceAnswerForm(forms.ModelForm):
#     class Meta:
#         model = SingleChoiceAnswer
#         fields = ['question', 'user', 'choice', 'is_readonly']
#         widgets = {
#             'question': forms.HiddenInput(),
#             'user': forms.HiddenInput(),
#             'is_readonly': forms.HiddenInput(),
#             'choice': forms.ChoiceField(
#                 attrs={'choices' : BookNode.objects.filter( node_type__in=['choice','correctchoice'] ).order_by('mpath'),
#             ),
#         }

# homework submission form (no visible fields)
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['user', 'assignment']
        widgets = {
            'user': forms.HiddenInput(),
            'assignment': forms.HiddenInput(),
        }
        

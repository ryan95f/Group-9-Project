from django import forms


class DeadlineForm(forms.Form):
    node = forms.CharField()
    date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd H:M'})
    )

    def clean_form(self):
        node = int(self.cleaned_data['node'])
        date = self.cleaned_data['date']
        return ({
            "node": node,
            "date": date
        })

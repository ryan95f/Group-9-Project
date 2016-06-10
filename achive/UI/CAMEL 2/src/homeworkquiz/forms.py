from django import forms


class DeadlineForm(forms.Form):
    """Form that is used to get deadline from the UI. Takes in the node
    and the date."""
    node = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    date = forms.DateTimeField(
        widget=forms.TextInput(attrs={'placeholder': 'yyyy-mm-dd H:M'})
    )

    def clean_form(self):
        """Method to clean all data that has been entered
        from the form"""
        node = int(self.cleaned_data['node'])
        date = self.cleaned_data['date']
        return ({
            "node": node,
            "date": date
        })

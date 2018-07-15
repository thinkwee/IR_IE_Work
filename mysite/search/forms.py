from django import forms


class AddForm(forms.Form):
    # a = forms.IntegerField()
    # b = forms.IntegerField()
    keywords = forms.CharField(widget=forms.TextInput(attrs={'size': '40'}))

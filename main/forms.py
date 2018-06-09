from django import forms


class MyUserForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'narrow-input', 'required': 'true'}),
                               required=True,
                               help_text='Password must be 8 characters minimum length (with at least 1 lower case, 1 upper case and 1 number).')
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'narrow-input', 'required': 'true'}),
                                       required=True, )

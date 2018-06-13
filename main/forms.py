from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
   Klasa reprezentująca formularz do logowania

   Atrybuty:
       username    Nazwa użytkownika
       password    Hasło użytkownika
   """
    username = forms.CharField(label='User name')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')


class RegisterUserForm(forms.ModelForm):
    """
   Klasa reprezentująca formularz do rejestrowania użytkownika

   Atrybuty:
       password            Hasło użytkownika
       password_confirm    Powtórzone hasło użytkownika
   """
    password = forms.CharField(widget=forms.PasswordInput(), label='Password',
                               help_text='Password must have from 6 to 20 characters.')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    class Meta:
        """
       Atrybuty:
           model           Określamy model, za pomocą którego zostanie wygenerowany formularz
           fields          Określamy pola, które chcemy użyć z tego modelu
           labels          Określamy nazwy etykiet naszych pobranych pól
           help_texts      Definiujemy tekts pomocniczy wyświetlany przy danym polu
           error_messages  Nadpisujemy nazwy błędów
       """
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        labels = {
            'username': 'Username',
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
        }
        help_texts = {
            'username': 'Username must have from 6 to 20 characters.',
            'email': 'Recommended from domain fis.agh.edu.pl.'
        }
        error_messages = {
            'username': {
                'unique': 'This user already exists!',
                'invalid': 'Wrong sign. Try another name!'
            },
            'email': {
                'invalid': 'Wrong email!'
            }
        }

    def __init__(self, *args, **kwargs):
        """
       Nadpisujemy metodę bazową do inicjalizacji obiektu
       Wszystkie pola klasy User będą wymagane, aby je dodać
       :param args:
       :param kwargs:
       """
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True

    def clean_username(self):
        """
       Sprawdza czy użytkownik podał wymaganą ilość znaków
       :return: username
       """
        username = self.cleaned_data['username'].strip()
        if len(username) < 4 or len(username) > 20:
            raise forms.ValidationError('Wrong characters number!')
        return username

    def clean_email(self):
        """
       Sprawdzamy, czy dany adres email istnieje już w bazie
       :return: email
       """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered!')
        return email

    def clean_password_confirm(self):
        """
       Sprawdzamy czy hasło zostało dwukrotnie podane prawidłowo
       Sprawdzamy czy hasło ma określoną ilość znaków
       :return: password
       """
        cd = self.cleaned_data
        password = cd['password']
        password_confirm = cd['password_confirm']
        if len(password) < 6 or len(password_confirm) > 20:
            raise forms.ValidationError('Invalid number of characters!')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match!')
        return password_confirm

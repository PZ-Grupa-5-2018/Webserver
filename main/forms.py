from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
   Klasa reprezentująca formularz do logowania

   Atrybuty:
       username    Nazwa użytkownika
       password    Hasło użytkownika
   """
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło')


class RegisterUserForm(forms.ModelForm):
    """
   Klasa reprezentująca formularz do rejestrowania użytkownika

   Atrybuty:
       password            Hasło użytkownika
       password_confirm    Powtórzone hasło użytkownika
   """
    password = forms.CharField(widget=forms.PasswordInput(), label='Hasło',
                               help_text='Hasło powinno zawierać od 6 do 20 znaków.')
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label='Powtórz hasło')

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
            'username': 'Nazwa użytkownika',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
            'email': 'Email',
        }
        help_texts = {
            'username': 'Nazwa użytkownika powinna zawierać od 6 do 20 znaków.',
            'email': 'Zalecany z domeny fis.agh.edu.pl.'
        }
        error_messages = {
            'username': {
                'unique': 'Taki użytkownik już istnieje!',
                'invalid': 'Niedozwolony znak. Spróbuj użyć innej nazwy!'
            },
            'email': {
                'invalid': 'Nieprawidłowy adres email!'
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
            raise forms.ValidationError('Nieprawidłowa liczba znaków!')
        return username

    def clean_email(self):
        """
       Sprawdzamy, czy dany adres email istnieje już w bazie
       :return: email
       """
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Taki adres email jest już zarejestrowany!')
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
            raise forms.ValidationError('Nieprawidłowa liczba znaków!')
        if password != password_confirm:
            raise forms.ValidationError('Hasła nie pasują!')
        return password_confirm

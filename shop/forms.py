from django import forms
from .models import LoginPerson, Contact


#  SIGNIN FORM
class SignInForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your First Name'}
        ))
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Last Name'}
        ))
    email = forms.CharField(
        max_length=50,
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Email example@domain.com'}
        ))
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Password'}
        ))
    phone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Phone No.'}
        ))
    address1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Address line1'}
        ))
    address2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Address line 2'}
        ))
    city = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your City'}
        ))
    state = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your State'}
        ))
    zip_code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Enter Your Zip Code'}
        ))

    class Meta:
        model = LoginPerson
        fields = '__all__'

#  LOGIN FORM


class LoginForm(forms.Form):
    email = forms.CharField(
        label='',
        max_length=100,
        widget=forms.EmailInput(
            attrs={'class': 'form-control',
                   'required': False,
                   'autofocus': True,
                   'placeholder': 'Email (example@domain.com)',
                   }
        ))

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Password'}
        ))


# ConntactUs Form
class ContactForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control'})
    )
    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(
            attrs={'class': 'form-control'})
    )
    phone = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control'})
    )
    desc = forms.CharField(
        label='How may i help you',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 10})
    )

    class Meta:
        model = Contact
        fields = ('name', 'email', 'phone', 'desc')

from django import forms
from .models import Contact, Blogpost

# login Form


class LoginForm(forms.Form):
    username = forms.CharField(
        label='',
        max_length=100,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Username'}
        ))
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter Password'}
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


# PostBlog Form
class BlogPostForm(forms.ModelForm):
    category = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'required': 'true'})
    )
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        max_length=30000,
        widget=forms.TextInput(attrs={
            'type': 'hidden'
        })
    )
    author = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'type': 'hidden'
        })
    )
    thumbnail = forms.FileField(
        label='Upload Thumbnail For Your Blog'
    )

    class Meta:
        model = Blogpost
        fields = ('category', 'title', 'content', 'author',
                  'description', 'thumbnail')

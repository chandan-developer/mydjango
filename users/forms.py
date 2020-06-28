from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Scraping
from random import randint


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    num1, num2 = randint(0,10),randint(0,10)
    captcha_value = num1 + num2
    
    captcha = forms.IntegerField(label=f'Are you human?<br> {num1} + {num2} = ?',required=True)
    captcha_value = forms.CharField(widget=forms.HiddenInput(),initial=captcha_value)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class FrequencyForm(forms.ModelForm):
    url = forms.URLField(required=True)

    class Meta:
        model = Scraping
        fields = ['url']


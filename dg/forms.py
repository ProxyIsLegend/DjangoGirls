from django import forms
from django.contrib.auth.models import User


class SendMessageFrom(forms.Form):
    text = forms.CharField(max_length=500)
    chat_id = forms.IntegerField()


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=500)
    new_password = forms.CharField(max_length=500)


class CreateChatForm(forms.Form):
    user_to = forms.CharField(max_length=1000, label='Username')


class UserRegistrationForm(forms.ModelForm):
    """This class provide you an opportunity to register on the site
        fields:
        password - password to your account
        password2 - repeat the password
        methods:
        clean_password2 - function that clean the field? if the passwords didn`t match
    """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        """This class adds you a username"""
        model = User
        fields = ('username', 'email', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

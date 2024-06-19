from django import forms
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper


from . import models


class UserForm(forms.ModelForm):
    email = forms.EmailField()    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )
        help_texts = {
            'username': None
        }



class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.exclude(
            pk=self.instance.pk).filter(email__iexact=email)
        if qs.exists():
            raise ValidationError(
                'A user with this email address already exists.')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password Confirmation'

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.exclude(
            pk=self.instance.pk).filter(email__iexact=email)
        if qs.exists():
            raise ValidationError(
                'A user with this email address already exists.')
        return email


class AddCredentialForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'credential_name',
            'credential_url',
            'credential_login',
            AppendedText('credential_password', mark_safe(
                '<i class="fa-solid fa-eye-slash" id="togglePassword" style="cursor: pointer;"></i>')),
            self.helper.add_input(Submit('submit', 'Add credential'))    
        )
        self.edit_helper = FormHelper()
        self.edit_helper.form_tag = False 
        self.edit_helper.layout = Layout(
            AppendedText('credential_password', mark_safe(
                '<i class="fa-solid fa-eye-slash" id="togglePassword" style="cursor: pointer;"></i>')),

        )

    class Meta:
        model = models.Credential
        fields = ('credential_name', 'credential_url', 'credential_login',
                  'credential_password',)
        labels = {
            'credential_name': 'Website or app name',
            'credential_url': 'Link to the website',
            'credential_login': 'Email or login',
            'credential_password': 'Password'
        }
        widgets = {
            'credential_password': forms.PasswordInput(),
        }

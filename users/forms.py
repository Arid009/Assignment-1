from django import forms
import re
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import Permission, Group
from events.forms import StyledFormMixin
from users.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomRegistrationForm(StyledFormMixin, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'password1', 'email']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")

        return email


    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')
        
        if errors:
            raise forms.ValidationError(errors)
        
        return password1

class LoginForm(StyledFormMixin,AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Assign Permission'
    )
    
    class Meta:
        model = Group
        fields = ['name', 'permissions']

class AssignRoleForm(StyledFormMixin, forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )

class EditProfileForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','phone_number','profile_image']

class CustomPasswordChangeForm(StyledFormMixin, PasswordChangeForm):
    pass


class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass


class CustomPasswordResetConfirmForm(StyledFormMixin, SetPasswordForm):
    pass
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomUser
from allauth.account.forms import SignupForm
from django import forms
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'birth_date']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone_number', 'birth_date']


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30, 
        label='First Name', 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'نام'})
    )
    last_name = forms.CharField(
        max_length=30, 
        label='Last Name', 
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'نام خانوادگی'})
    )
    phone_number = forms.CharField(
        max_length=11,
        label='Phone Number',
        required=False,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره تلفن باید با 09 شروع شود و 11 رقم باشد')],
        widget=forms.TextInput(attrs={'placeholder': 'شماره تلفن'})
    )
    birth_date = forms.DateField(
        label='Birth Date',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def save(self, request):
        # First, call the parent save method to create the user
        user = super(CustomSignupForm, self).save(request)
        
        # Now save the additional fields
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.phone_number = self.cleaned_data.get('phone_number', '')
        user.birth_date = self.cleaned_data.get('birth_date')
        
        # Save the user with the new fields
        user.save()
        
        return user
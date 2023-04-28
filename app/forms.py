from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm,AuthenticationForm,PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from .models import *
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        

class LoginForm(AuthenticationForm):
     username=forms.CharField(label='Email address',widget=forms.TextInput
                             (attrs={'autofocus':"True",'placeholder':'email address','class':"form-control"}))
    
     password=forms.CharField(label='Password',widget=forms.PasswordInput
                             (attrs={'placeholder':'password','autocomplete':'current-password','class':'form-control'}))
     
     class Meta:
        model=CustomUser
        fields=['email','password']
    

class RegistrationForm(UserCreationForm):
    
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    
    email=forms.CharField(label='Email',widget=forms.EmailInput
                          (attrs={'class':'form-control'}))
    
    password1=forms.CharField(label='Create Password',widget=forms.PasswordInput
                             (attrs={'class':'form-control'}))
    
    password2=forms.CharField(label='Confirm Password',widget=forms.PasswordInput
                             (attrs={'class':'form-control'}))
    
    class Meta:
        model=CustomUser
        fields=['name','email','password1','password2']
        
class ChangePasswordForm(PasswordChangeForm):
    old_pass=forms.CharField(label="User Old Password",widget=forms.PasswordInput
    (attrs={'autofocus':True,'class':"form-control"}))
    new_pass1=forms.CharField(label="User New Password",widget=forms.PasswordInput
    (attrs={'class':'form-control'}))
    new_pass2=forms.CharField(label="User Confirm Password",widget=forms.PasswordInput
    (attrs={'class':'form-control'}))
  
      
class ResetPasswordForm(PasswordResetForm):
     email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
 
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=['name','locality','city','mobile','state','zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control','required':False}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'mobile': forms.NumberInput(attrs={'class':'form-control','minlength': 10, 'maxlength': 15, 'required': True, 'type': 'number',}),             
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control','required':False}),
        }
    
class SetPasswordForm(SetPasswordForm):
    new_pass1=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password','class':'form-control'}))
    new_pass2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={
        'autocomplete':'current-password','class':'form-control'}))
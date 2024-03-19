from .models import NewUser, Influencerinfo, Customer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms 
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation




class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    user_phonenumber = forms.IntegerField(label='Contact Number', widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = NewUser
        fields = ['email', 'user_phonenumber', 'password1', 'password2']
        labels = {'email': 'Email'}
        # widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


class  LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus':True, 'class':'form-control'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    influencercode = forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-control'}))

    



    '''def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')'''






class InfluencerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    user_phonenumber = forms.IntegerField(label='Contact Number', widget=forms.NumberInput(attrs={'class':'form-control'}))
    influencerinstagram = forms.CharField(label='Instagram', widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = NewUser
        fields = [ 'influencerinstagram', 'email', 'user_phonenumber', 'password1', 'password2']
        labels = {'email': 'Email'}
        # widgets = {'username': forms.TextInput(attrs={'class':'form-control'})}


class  InfluencerLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True, 'class':'form-control'}))
    user_phonenumber = forms.CharField(label='Contact Number', widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))
    influencercode = forms.CharField(widget=forms.TextInput(attrs={ 'class':'form-control'}))


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'state', 'zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                   'locality':forms.TextInput(attrs={'class':'form-control'}),
                   'city':forms.TextInput(attrs={'class': 'form-control'}), 
                   'state':forms.Select(attrs={'class':'form.control'}), 
                   'zipcode':forms.NumberInput(attrs={'class':'form-control'})}


















class InfluencerSignUpForm(forms.ModelForm):
   
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
      model=Influencerinfo
      fields=['influencer_name','influencer_email','influencer_phone','password','confirm_password']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

class InflencerLoginForm(forms.Form):
    influencer_email = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput())
    influencer_code=forms.CharField(max_length=15)

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',  'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email', 'class':'form-control'}))


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'new-password',  'class':'form-control'}))

from django.forms import ModelForm
from .models import Product
from django import forms
from .models import Product

class SellerForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'factory', 'product_image', 'product_image2', 'product_image3', 'size', 'colors']
        widgets = {
            'product_image': forms.ClearableFileInput(attrs={'multiple': True}),
            'product_image2': forms.ClearableFileInput(attrs={'multiple': True}),
            'product_image3': forms.ClearableFileInput(attrs={'multiple': True}),
        }
        labels = {
            'title': 'Product Title',
            'selling_price': 'Price',
            'product_image': 'Product Image 1',
            'product_image2': 'Product Image 2',
            'product_image3': 'Product Image 3',
            'size': 'Sizes Available',
            'colors': 'Colors Available',
            'factory':'Shop Name',
        }
        required = {
            'title': True,
            'selling_price': True,
            'product_image': True,
            'product_image2': True,
            'product_image3': True,
            'size': True,
            'colors': True,
            'factory': True,
        }

    def __init__(self, *args, **kwargs):
        super(SellerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

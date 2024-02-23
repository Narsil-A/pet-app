from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.db import transaction
from userprofile.models import User, VetStaff, PetOwner




class VetStaffSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    image = forms.ImageField(required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md', 'onfocus': 'showPasswordConditions()'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}),
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'image', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vetstaff = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            vetstaff = VetStaff.objects.create(user=user)
            vetstaff.image = self.cleaned_data.get('image')
            vetstaff.save()
        return user

class PetOwnerSignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    image = forms.ImageField(required=False)
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md', 'onfocus': 'showPasswordConditions()'}),
        required=True
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','email', 'image', 'password1', 'password2']
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_petowner = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            petowner = PetOwner.objects.create(user=user)
            petowner.image = self.cleaned_data.get('image')
            petowner.save()
        return user
class VetStaffEditForm(UserChangeForm):
    password = None 
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    image = forms.ImageField(required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    country = forms.ChoiceField(choices=User.COUNTRY_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number', 'image', 'state', 'country', 'city', 'zip_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_vetstaff = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.state = self.cleaned_data.get('state')
        user.country = self.cleaned_data.get('country')
        user.city = self.cleaned_data.get('city')
        user.zip_code = self.cleaned_data.get('zip_code')
        user.position = self.cleaned_data.get('position')
        if commit:
            user.save()
            user.vetstaff.image = self.cleaned_data.get('image')
            user.vetstaff.save()
        return user
class PetOwnerEditForm(UserChangeForm):
    password = None 
    image = forms.ImageField(required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}))
    image = forms.ImageField(required=False)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    state = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    country = forms.ChoiceField(choices=User.COUNTRY_CHOICES, required=False, widget=forms.Select(attrs={
        'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'type': 'tel', 'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=False)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address', 'phone_number', 'image', 'state', 'country', 'city', 'zip_code']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_petowner = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.state = self.cleaned_data.get('state')
        user.country = self.cleaned_data.get('country')
        user.city = self.cleaned_data.get('city')
        user.zip_code = self.cleaned_data.get('zip_code')
        if commit:
            user.save()
            user.petowner.image = self.cleaned_data.get('image')
            user.petowner.save()
        return user

class PasswordChangeForm(forms.Form):
    current_password = forms.CharField(label="Current Password", widget=forms.PasswordInput())
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="Confirm New Password", widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Your current password was entered incorrectly.")
        return current_password

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        password_validation.validate_password(new_password, self.user)
        return new_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")

        return cleaned_data

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from userprofile.models import User, VetStaff



class VetStaffSignUpForm(UserCreationForm):
    position = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    degrees = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
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
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_vetstaff = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.save()
        VetStaff.objects.create(
            user=user,
            position=self.cleaned_data.get('position'),
            profession=self.cleaned_data.get('profession'),
            degrees=self.cleaned_data.get('degrees')
        )
        return user



class PetOwnerSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full py-1 px-2 my-1 text-sm border border-gray-300 rounded-md'}), required=True)
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
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_petowner = True
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.address = self.cleaned_data.get('address')
        user.save()
        return user

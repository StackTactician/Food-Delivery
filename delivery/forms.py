from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, MenuItem

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('Customer', 'Customer'), ('Driver', 'Driver')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    # Extra fields for UserProfile
    phone_number = forms.CharField(max_length=15, required=True, label="Phone Number")
    profile_photo = forms.ImageField(required=False, label="Profile Photo")
    
    # Customer Fields
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, label="Home/Delivery Address")
    
    # Driver Fields
    license_number = forms.CharField(max_length=50, required=False, label="Driver's License Number")
    vehicle_plate = forms.CharField(max_length=20, required=False, label="Vehicle Plate Number")
    vehicle_type = forms.CharField(max_length=50, required=False, label="Vehicle Type")
    bank_account = forms.CharField(max_length=50, required=False, label="Bank Account for Payouts")
    is_available = forms.BooleanField(required=False, label="Available for deliveries immediately?", initial=False)

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        
        if role == 'Customer':
            if not cleaned_data.get('address'):
                self.add_error('address', 'Address is required for customers.')
        
        elif role == 'Driver':
            if not cleaned_data.get('license_number'):
                self.add_error('license_number', 'License number is required for drivers.')
            if not cleaned_data.get('vehicle_plate'):
                self.add_error('vehicle_plate', 'Vehicle plate is required for drivers.')
            if not cleaned_data.get('vehicle_type'):
                self.add_error('vehicle_type', 'Vehicle type is required for drivers.')
            if not cleaned_data.get('bank_account'):
                self.add_error('bank_account', 'Bank account is required for drivers.')
        
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone_number

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            profile = UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                phone_number=self.cleaned_data.get('phone_number'),
                profile_photo=self.cleaned_data.get('profile_photo'),
                address=self.cleaned_data.get('address'),
                license_number=self.cleaned_data.get('license_number'),
                vehicle_plate=self.cleaned_data.get('vehicle_plate'),
                vehicle_type=self.cleaned_data.get('vehicle_type'),
                bank_account=self.cleaned_data.get('bank_account'),
                is_available=self.cleaned_data.get('is_available')
            )
        return user

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'phone_number', 'address', 'vehicle_type', 'vehicle_plate', 'license_number']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        if self.instance.user:
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(UserProfileForm, self).save(commit=False)
        if commit:
            profile.save()
            # Update User email
            user = profile.user
            user.email = self.cleaned_data['email']
            user.save()
        return profile

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image']

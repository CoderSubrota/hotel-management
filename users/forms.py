from django import forms
from users.models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password"
    )
    
    profile_picture = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        label="Profile Picture"
    )

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','username', 'email', 'password', 'profile_picture','balance']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'balance':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your new balance'})
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class DepositForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label='Deposit Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount to deposit'})
    )
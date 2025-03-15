from django import forms
from hotels.models import Booking, Review,Hotel

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        
        
class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name', 'address', 'image', 'price_per_night', 'available_rooms']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter hotel name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price per night'}),
            'available_rooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available rooms'}),
        }
        
        
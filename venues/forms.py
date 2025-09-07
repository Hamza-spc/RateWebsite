from django import forms
from .models import Venue, Rating, ContactMessage, Category


class VenueForm(forms.ModelForm):
    """Form for creating and editing venues"""
    
    class Meta:
        model = Venue
        fields = [
            'name', 'description', 'category', 'address', 'city', 'country',
            'latitude', 'longitude', 'phone', 'email', 'website',
            'price_range_min', 'price_range_max', 'currency',
            'booking_com_link', 'trip_com_link', 'facilities',
            'languages_spoken', 'amenities', 'is_active', 'is_featured'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'price_range_min': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'price_range_max': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 3}),
            'booking_com_link': forms.URLInput(attrs={'class': 'form-control'}),
            'trip_com_link': forms.URLInput(attrs={'class': 'form-control'}),
            'facilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter facilities separated by commas'}),
            'languages_spoken': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter languages separated by commas'}),
            'amenities': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter amenities separated by commas'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make some fields optional
        self.fields['latitude'].required = False
        self.fields['longitude'].required = False
        self.fields['phone'].required = False
        self.fields['email'].required = False
        self.fields['website'].required = False
        self.fields['price_range_min'].required = False
        self.fields['price_range_max'].required = False
        self.fields['booking_com_link'].required = False
        self.fields['trip_com_link'].required = False
    
    def clean_facilities(self):
        facilities = self.cleaned_data.get('facilities')
        if facilities:
            # Convert string to list
            if isinstance(facilities, str):
                facilities = [f.strip() for f in facilities.split(',') if f.strip()]
        return facilities
    
    def clean_languages_spoken(self):
        languages = self.cleaned_data.get('languages_spoken')
        if languages:
            # Convert string to list
            if isinstance(languages, str):
                languages = [l.strip() for l in languages.split(',') if l.strip()]
        return languages
    
    def clean_amenities(self):
        amenities = self.cleaned_data.get('amenities')
        if amenities:
            # Convert string to list
            if isinstance(amenities, str):
                amenities = [a.strip() for a in amenities.split(',') if a.strip()]
        return amenities


class RatingForm(forms.ModelForm):
    """Form for rating venues"""
    
    class Meta:
        model = Rating
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].required = True
        self.fields['comment'].required = False


class ContactForm(forms.ModelForm):
    """Form for contact messages"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message...'}),
        }


class SearchForm(forms.Form):
    """Form for searching venues"""
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'What are you looking for?'
        })
    )
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Location'
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

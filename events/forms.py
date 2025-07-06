from django import forms
from .models import Event
from django.utils import timezone

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'end_date', 'ticket_price']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be after start date.")
            
            if start_date < timezone.now():
                raise forms.ValidationError("Start date cannot be in the past.")
        
        return cleaned_data

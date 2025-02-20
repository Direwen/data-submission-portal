from django import forms
from .models import DataEntry

class DataEntryForm(forms.ModelForm):
    class Meta:
        model = DataEntry
        fields = ['content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter content here'}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border rounded-md focus:ring-2 focus:ring-blue-500'}),
        }

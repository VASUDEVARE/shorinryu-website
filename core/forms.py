from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model  = ContactMessage
        fields = ['first_name', 'last_name', 'email', 'phone', 'program', 'age_group', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add placeholder and styling to every field
        placeholders = {
            'first_name': 'Your first name',
            'last_name':  'Your last name',
            'email':      'your@email.com',
            'phone':      '+91 XXXXX XXXXX',
            'message':    'Tell us about your goals, experience level, or any questions...',
        }
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-field'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]

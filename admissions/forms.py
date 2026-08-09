from django import forms

from courses.models import Course

from .models import AdmissionApplication


class AdmissionApplicationForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        empty_label='Select a course',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = AdmissionApplication
        fields = [
            'full_name',
            'father_name',
            'email',
            'phone',
            'whatsapp_number',
            'city',
            'country',
            'course',
            'course_interested',
            'education',
            'occupation',
            'preferred_contact_method',
            'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's name (optional)"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your country'}),
            'course_interested': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'If your course is not listed above, name it here',
            }),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Highest qualification'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current occupation (optional)'}),
            'preferred_contact_method': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Anything else you would like us to know'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        course_interested = cleaned_data.get('course_interested')

        if not course and not course_interested:
            raise forms.ValidationError(
                'Please select a course from the list or tell us which course you are interested in.'
            )

        return cleaned_data

from django import forms

from courses.models import Course

from .models import Inquiry


class InquiryForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.filter(is_active=True),
        required=False,
        empty_label='Select a course (optional)',
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Inquiry
        fields = ['full_name', 'phone', 'email', 'course', 'course_interested', 'message']

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone / WhatsApp number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'course_interested': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course you are interested in'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your message'}),
        }

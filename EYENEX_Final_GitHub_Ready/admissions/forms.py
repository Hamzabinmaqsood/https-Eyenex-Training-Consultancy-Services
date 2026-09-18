from datetime import date

from django import forms

from courses.models import Course

from .models import AdmissionApplication, CourseAppointment


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


class CourseAppointmentForm(forms.ModelForm):
    class Meta:
        model = CourseAppointment
        fields = [
            'full_name',
            'email',
            'phone',
            'whatsapp_number',
            'city',
            'preferred_date',
            'preferred_time',
            'financial_aid_requested',
            'financial_aid_reason',
            'payment_screenshot',
            'message',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your phone number'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp number (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your city'}),
            'preferred_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'preferred_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'financial_aid_requested': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'financial_aid_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please explain why you need financial aid for the appointment fee.',
            }),
            'payment_screenshot': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/png,image/jpeg,image/webp',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Any additional details for your appointment (optional)',
            }),
        }

    def __init__(self, *args, course=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course
        self.fields['payment_screenshot'].required = False
        self.fields['financial_aid_reason'].required = False
        self.fields['preferred_date'].widget.attrs['min'] = date.today().isoformat()

    def clean_preferred_date(self):
        preferred_date = self.cleaned_data.get('preferred_date')
        if preferred_date and preferred_date < date.today():
            raise forms.ValidationError('Please choose today or a future date.')
        return preferred_date

    def clean(self):
        cleaned_data = super().clean()
        financial_aid_requested = cleaned_data.get('financial_aid_requested')
        financial_aid_reason = (cleaned_data.get('financial_aid_reason') or '').strip()
        payment_screenshot = cleaned_data.get('payment_screenshot')

        if financial_aid_requested:
            cleaned_data['payment_screenshot'] = None
            if not financial_aid_reason:
                self.add_error(
                    'financial_aid_reason',
                    'Please tell us why you need financial aid for the appointment fee.',
                )
        else:
            cleaned_data['financial_aid_reason'] = ''
            if self.course and self.course.appointment_fee > 0 and not payment_screenshot:
                self.add_error(
                    'payment_screenshot',
                    'Please upload one screenshot of your appointment-fee payment.',
                )

        return cleaned_data

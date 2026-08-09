import hashlib

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from inquiries.forms import InquiryForm
from courses.models import Course
from testimonials.models import Testimonial
from faqs.models import FAQ

DUPLICATE_SUBMISSION_WINDOW_SECONDS = 60

def home(request):
    featured_courses = Course.objects.filter(is_active=True, is_featured=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    faqs = FAQ.objects.filter(is_active=True)[:6]

    context = {
        'featured_courses': featured_courses,
        'testimonials': testimonials,
        'faqs': faqs,
    }

    return render(request, 'core/home.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    selected_course = request.GET.get('course', '')

    if request.method == 'POST':
        form = InquiryForm(request.POST)

        if form.is_valid():
            course = form.cleaned_data.get('course')
            fingerprint = hashlib.sha256(
                '|'.join([
                    form.cleaned_data['full_name'].strip().lower(),
                    form.cleaned_data['phone'].strip(),
                    str(course.pk if course else form.cleaned_data.get('course_interested', '')),
                ]).encode()
            ).hexdigest()

            now = timezone.now().timestamp()
            is_duplicate = (
                request.session.get('last_inquiry_fingerprint') == fingerprint
                and now - request.session.get('last_inquiry_time', 0) < DUPLICATE_SUBMISSION_WINDOW_SECONDS
            )

            if not is_duplicate:
                form.save()
                request.session['last_inquiry_fingerprint'] = fingerprint
                request.session['last_inquiry_time'] = now

            messages.success(request, 'Your inquiry has been submitted successfully. Our team will contact you soon.')
            return redirect('core:contact')
        else:
            messages.error(request, 'Please correct the errors below and try again.')
    else:
        form = InquiryForm(initial={
            'course_interested': selected_course
        })

    return render(request, 'core/contact.html', {'form': form})


def ielts(request):
    return render(request, 'core/ielts.html')


def study_abroad(request):
    return render(request, 'core/study_abroad.html')


def leadership(request):
    return render(request, 'core/leadership.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def terms(request):
    return render(request, 'core/terms.html')

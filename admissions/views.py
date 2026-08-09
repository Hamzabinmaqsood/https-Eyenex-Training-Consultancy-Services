import hashlib

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from courses.models import Course

from .forms import AdmissionApplicationForm

DUPLICATE_SUBMISSION_WINDOW_SECONDS = 60


def admissions(request):
    return render(request, 'admissions/admissions.html')


def apply(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)

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
                request.session.get('last_application_fingerprint') == fingerprint
                and now - request.session.get('last_application_time', 0) < DUPLICATE_SUBMISSION_WINDOW_SECONDS
            )

            if not is_duplicate:
                form.save()
                request.session['last_application_fingerprint'] = fingerprint
                request.session['last_application_time'] = now

            messages.success(
                request,
                'Your application has been submitted successfully. Our admissions team will contact you soon.',
            )
            return redirect('admissions:apply')
    else:
        initial = {}
        course_slug = request.GET.get('course', '')

        if course_slug:
            course = Course.objects.filter(slug=course_slug, is_active=True).first()

            if course:
                initial['course'] = course
            else:
                initial['course_interested'] = course_slug

        form = AdmissionApplicationForm(initial=initial)

    return render(request, 'admissions/apply.html', {'form': form})

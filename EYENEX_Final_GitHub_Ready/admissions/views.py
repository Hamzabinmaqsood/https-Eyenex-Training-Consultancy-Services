import hashlib

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from courses.models import Course

from .forms import AdmissionApplicationForm, CourseAppointmentForm
from .models import CourseAppointment

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


def course_appointment(request, slug):
    course = get_object_or_404(Course, slug=slug, is_active=True)

    if request.method == 'POST':
        form = CourseAppointmentForm(request.POST, request.FILES, course=course)

        if form.is_valid():
            fingerprint = hashlib.sha256(
                '|'.join([
                    form.cleaned_data['full_name'].strip().lower(),
                    form.cleaned_data['phone'].strip(),
                    str(course.pk),
                    str(form.cleaned_data['preferred_date']),
                    str(form.cleaned_data['preferred_time']),
                ]).encode()
            ).hexdigest()

            now = timezone.now().timestamp()
            is_duplicate = (
                request.session.get('last_appointment_fingerprint') == fingerprint
                and now - request.session.get('last_appointment_time', 0) < DUPLICATE_SUBMISSION_WINDOW_SECONDS
            )

            if not is_duplicate:
                appointment = form.save(commit=False)
                appointment.course = course
                appointment.appointment_fee = course.appointment_fee
                appointment.save()
                request.session['last_appointment_fingerprint'] = fingerprint
                request.session['last_appointment_time'] = now

            messages.success(
                request,
                'Your appointment request has been submitted successfully. Our team will review it and contact you soon.',
            )
            return redirect('admissions:course_appointment', slug=course.slug)
    else:
        form = CourseAppointmentForm(course=course)

    return render(request, 'admissions/course_appointment.html', {
        'course': course,
        'form': form,
    })


# Sensitive payment receipts are stored outside the public media directory and
# are only available to authenticated staff through this protected endpoint.
@staff_member_required
def payment_receipt(request, pk):
    appointment = get_object_or_404(CourseAppointment, pk=pk)
    receipt = appointment.payment_screenshot
    if not receipt:
        raise Http404('No payment receipt was uploaded for this appointment.')
    try:
        return FileResponse(receipt.open('rb'), as_attachment=False, filename=receipt.name.rsplit('/', 1)[-1])
    except FileNotFoundError as exc:
        raise Http404('Payment receipt file not found.') from exc

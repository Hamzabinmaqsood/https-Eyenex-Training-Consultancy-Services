from decimal import Decimal

from django.db import migrations


def populate_course_details(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    CourseCategory = apps.get_model('courses', 'CourseCategory')

    professional_category, _ = CourseCategory.objects.get_or_create(
        name='Professional Development & Guidance',
        defaults={
            'slug': 'professional-development-guidance',
            'description': 'Career guidance, professional development, exam support, and consultancy designed to help individuals make stronger career decisions.',
        },
    )

    # All current courses can be attended physically or online unless an admin changes the setting later.
    Course.objects.all().update(delivery_mode='both')

    nebosh = Course.objects.filter(title__iexact='NEBOSH Preparation').first()
    if not nebosh:
        nebosh = Course.objects.filter(slug='nebosh-preparation').first()
    if nebosh:
        nebosh.title = 'NEBOSH IGC'
        nebosh.duration = '15 Days'
        nebosh.fee = Decimal('180000.00')
        nebosh.official_test_fee_included = True
        nebosh.delivery_mode = 'both'
        nebosh.save(update_fields=['title', 'duration', 'fee', 'official_test_fee_included', 'delivery_mode'])

    iosh = Course.objects.filter(title__icontains='IOSH').first()
    if iosh:
        iosh.fee = Decimal('35000.00')
        iosh.official_test_fee_included = True
        iosh.delivery_mode = 'both'
        iosh.save(update_fields=['fee', 'official_test_fee_included', 'delivery_mode'])

    osha = Course.objects.filter(title__icontains='OSHA').first()
    if osha:
        osha.fee = Decimal('22000.00')
        osha.official_test_fee_included = True
        osha.delivery_mode = 'both'
        osha.save(update_fields=['fee', 'official_test_fee_included', 'delivery_mode'])

    spoken, created = Course.objects.get_or_create(
        slug='spoken-english',
        defaults={
            'category': professional_category,
            'title': 'Spoken English',
            'short_description': 'Practical spoken English training focused on confidence, everyday communication, vocabulary, pronunciation, and professional conversation skills.',
            'description': 'Spoken English training helps learners build confidence in everyday and professional communication through guided speaking practice, vocabulary development, pronunciation support, listening activities, and practical conversation exercises.',
            'duration': '',
            'fee': Decimal('20000.00'),
            'official_test_fee_included': True,
            'delivery_mode': 'both',
            'level': 'beginner',
            'is_featured': False,
            'is_active': True,
            'display_order': 9,
        },
    )
    if not created:
        spoken.fee = Decimal('20000.00')
        spoken.official_test_fee_included = True
        spoken.delivery_mode = 'both'
        spoken.save(update_fields=['fee', 'official_test_fee_included', 'delivery_mode'])

    ielts, created = Course.objects.get_or_create(
        slug='ielts-preparation',
        defaults={
            'category': professional_category,
            'title': 'IELTS Preparation',
            'short_description': 'Structured IELTS preparation covering listening, reading, writing, and speaking with practice-focused guidance for test readiness.',
            'description': 'IELTS Preparation supports learners across the four test skills: Listening, Reading, Writing, and Speaking. The course focuses on test format awareness, time management, practice tasks, feedback, language improvement, and strategies for stronger test performance.',
            'duration': '',
            'fee': Decimal('90000.00'),
            'official_test_fee_included': True,
            'delivery_mode': 'both',
            'level': 'intermediate',
            'is_featured': False,
            'is_active': True,
            'display_order': 10,
        },
    )
    if not created:
        ielts.fee = Decimal('90000.00')
        ielts.official_test_fee_included = True
        ielts.delivery_mode = 'both'
        ielts.save(update_fields=['fee', 'official_test_fee_included', 'delivery_mode'])


def reverse_course_details(apps, schema_editor):
    # Deliberately keep user/admin-managed course data on rollback.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_course_appointment_fee_course_delivery_mode_and_more'),
    ]

    operations = [
        migrations.RunPython(populate_course_details, reverse_course_details),
    ]

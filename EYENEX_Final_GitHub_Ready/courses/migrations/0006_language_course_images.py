from django.db import migrations


def set_language_course_images(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')

    defaults = {
        'spoken-english': 'courses/spoken-english-instructor.png',
        'ielts-preparation': 'courses/ielts-preparation-instructor.png',
    }

    for slug, image_path in defaults.items():
        course = Course.objects.filter(slug=slug).first()
        if course and not course.image:
            course.image = image_path
            course.save(update_fields=['image'])


def reverse_language_course_images(apps, schema_editor):
    # Do not remove an admin-managed image during rollback.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_populate_course_details'),
    ]

    operations = [
        migrations.RunPython(set_language_course_images, reverse_language_course_images),
    ]

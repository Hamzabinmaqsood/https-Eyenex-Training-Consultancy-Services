import core.storage
import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0002_courseappointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseappointment',
            name='payment_screenshot',
            field=models.ImageField(
                blank=True,
                null=True,
                storage=core.storage.PrivateMediaStorage(),
                upload_to='appointments/payment_receipts/%Y/%m/',
                validators=[core.validators.validate_image_size],
            ),
        ),
    ]

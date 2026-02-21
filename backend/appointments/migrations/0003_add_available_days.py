from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0002_add_availability'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='available_days',
            field=models.CharField(default='0,1,2,3,4', help_text='Comma separated weekdays as numbers 0=Monday', max_length=32),
        ),
    ]

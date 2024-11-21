# Generated by Django 5.1.2 on 2024-10-20 01:43

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0005_alter_job_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='internship',
            new_name='Job',
        ),
        migrations.AddField(
            model_name='application',
            name='applied_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]

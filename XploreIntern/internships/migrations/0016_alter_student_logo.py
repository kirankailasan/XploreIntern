# Generated by Django 5.1.2 on 2024-11-09 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0015_employer_updated_at_student_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='logo',
            field=models.FileField(default='images/default_profile.jpg', null=True, upload_to='logo/'),
        ),
    ]

# Generated by Django 5.1.2 on 2024-11-17 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0028_application_employer_viewed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='employer_viewed',
        ),
    ]
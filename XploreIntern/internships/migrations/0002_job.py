# Generated by Django 5.1.1 on 2024-10-02 05:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('job_type', models.CharField(choices=[('Full-time', 'Full-Time'), ('Part-time', 'Part-Time'), ('Contract', 'Contract'), ('Temporary', 'Temporary')], max_length=50)),
                ('experience_level', models.CharField(choices=[('Entry-level', 'Entry-Level'), ('Junior', 'Junior'), ('Mid-level', 'Mid-Level'), ('Senior', 'Senior'), ('Executive', 'Executive')], max_length=50)),
                ('salary_range', models.CharField(max_length=100)),
                ('benefits', models.TextField()),
                ('summary', models.TextField()),
                ('key_responsibilities', models.TextField()),
                ('required_qualifications', models.TextField()),
                ('preferred_qualifications', models.TextField(blank=True)),
                ('skills', models.TextField()),
                ('application_instructions', models.TextField()),
                ('application_deadline', models.DateField()),
                ('contact_information', models.TextField()),
                ('company_overview', models.TextField()),
                ('company_website', models.URLField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

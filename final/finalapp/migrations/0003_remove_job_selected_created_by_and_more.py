# Generated by Django 4.2.3 on 2023-12-28 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0002_job_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job_selected',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='job_selected',
            name='job_id',
        ),
        migrations.DeleteModel(
            name='Hiring',
        ),
        migrations.DeleteModel(
            name='job_selected',
        ),
    ]

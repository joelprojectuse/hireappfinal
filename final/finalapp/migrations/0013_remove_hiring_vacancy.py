# Generated by Django 4.2.3 on 2024-01-04 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0012_alter_hiring_vacancy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hiring',
            name='vacancy',
        ),
    ]
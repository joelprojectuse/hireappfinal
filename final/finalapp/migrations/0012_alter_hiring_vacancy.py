# Generated by Django 4.2.3 on 2024-01-04 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0011_hiring_vacancy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiring',
            name='vacancy',
            field=models.PositiveIntegerField(),
        ),
    ]

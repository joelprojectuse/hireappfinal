# Generated by Django 4.2.3 on 2024-01-21 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finalapp', '0024_customuser_ploc1_customuser_ploc2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('jober', 'Jober'), ('hirer', 'Hirer')], default='jober', max_length=15),
        ),
    ]

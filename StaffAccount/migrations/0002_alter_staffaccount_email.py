# Generated by Django 4.0.5 on 2022-06-13 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StaffAccount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffaccount',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]

# Generated by Django 4.0.5 on 2022-06-19 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resident', '0003_rename_user_usercompliant_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercompliant',
            old_name='user_id',
            new_name='user',
        ),
    ]
# Generated by Django 5.1.5 on 2025-02-10 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0042_remove_userinfo_about_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userinfo',
            old_name='dev_story',
            new_name='about_user',
        ),
    ]

# Generated by Django 5.2.1 on 2025-05-25 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0100_alter_post_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_project',
            name='media',
            field=models.ImageField(blank=True, null=True, upload_to='user-project-files'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-29 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_alter_projects_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='projects',
            name='github_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]

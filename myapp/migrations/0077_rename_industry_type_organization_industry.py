# Generated by Django 5.1.5 on 2025-03-26 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0076_industry_remove_organization_industry_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='industry_type',
            new_name='industry',
        ),
    ]

# Generated by Django 5.1.5 on 2025-05-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0087_alter_userinfo_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='needs_profile_completion',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='domains',
            field=models.ManyToManyField(blank=True, to='myapp.domain', verbose_name='domains'),
        ),
    ]

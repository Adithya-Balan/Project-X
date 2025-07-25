# Generated by Django 5.1.5 on 2025-02-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0052_alter_post_aspect'),
    ]

    operations = [
        migrations.AddField(
            model_name='current_position',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='current_position',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='current_position',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user_project',
            name='description',
            field=models.TextField(null=True),
        ),
    ]

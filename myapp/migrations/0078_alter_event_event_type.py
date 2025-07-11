# Generated by Django 5.1.5 on 2025-03-26 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0077_rename_industry_type_organization_industry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('webinar', 'Webinar'), ('workshop', 'Workshop'), ('conference', 'Conference'), ('meetup', 'Meetup'), ('hackathon', 'Hackathon'), ('bootcamp', 'Bootcamp'), ('startup-pitch', 'Startup Pitch'), ('networking', 'Networking'), ('other', 'Other')], default='other', max_length=20),
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-08 06:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_organization_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('event_type', models.CharField(choices=[('webinar', 'Webinar'), ('workshop', 'Workshop'), ('conference', 'Conference'), ('meetup', 'Meetup'), ('hackathon', 'Hackathon'), ('other', 'Other')], default='other', max_length=20)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('banner', models.ImageField(help_text='Optional image for the event.', upload_to='events')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='myapp.organization')),
            ],
        ),
        migrations.CreateModel(
            name='post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='user-posts')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('Organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_post', to='myapp.organization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_post', to='myapp.userinfo')),
            ],
        ),
    ]

# Generated by Django 5.1.5 on 2025-02-14 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0051_alter_post_aspect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='aspect',
            field=models.CharField(choices=[('Original', 'Original'), ('1:1', '1:1'), ('16:9', '16:9')], default='16:9', max_length=10),
        ),
    ]

# Generated by Django 5.1.5 on 2025-01-28 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_alter_user_project_tech_stack'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='category',
            field=models.CharField(choices=[('Programming Language', 'Programming Language'), ('Framework', 'Framework'), ('Tool', 'Tool'), ('Database', 'Database'), ('Cloud Platform', 'Cloud Platform'), ('Version Control', 'Version Control'), ('DevOps', 'DevOps'), ('UI/UX Design', 'UI/UX Design'), ('Machine Learning', 'Machine Learning'), ('Web Development', 'Web Development')], default='Programming Language', max_length=50),
        ),
    ]

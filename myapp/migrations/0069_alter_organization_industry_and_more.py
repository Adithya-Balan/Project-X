# Generated by Django 5.1.5 on 2025-03-12 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0068_alter_event_event_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='industry',
            field=models.CharField(choices=[('Software & IT Services', 'Software & IT Services'), ('Artificial Intelligence & Machine Learning', 'Artificial Intelligence & Machine Learning'), ('Cloud Computing & Infrastructure', 'Cloud Computing & Infrastructure'), ('Cybersecurity', 'Cybersecurity'), ('Blockchain, Crypto & Web3', 'Blockchain, Crypto & Web3'), ('Game Development', 'Game Development'), ('Financial Technology (Fintech)', 'Financial Technology (Fintech)'), ('Education Technology', 'Education Technology'), ('Healthcare & Medical Technology', 'Healthcare & Medical Technology'), ('Hardware & Electronics', 'Hardware & Electronics'), ('Telecommunications', 'Telecommunications'), ('E-commerce & Retail Tech', 'E-commerce & Retail Tech'), ('Marketing & Advertising Technology', 'Marketing & Advertising Technology'), ('Media & Entertainment', 'Media & Entertainment'), ('Automotive & Mobility Tech', 'Automotive & Mobility Tech'), ('Aerospace & Defense', 'Aerospace & Defense'), ('IoT, Robotics & Automation', 'IoT, Robotics & Automation'), ('GreenTech & Sustainable Energy', 'GreenTech & Sustainable Energy'), ('Augmented Reality & Virtual Reality', 'Augmented Reality & Virtual Reality'), ('Government & Public Sector', 'Government & Public Sector'), ('Defense & Military', 'Defense & Military'), ('Law Enforcement & Security', 'Law Enforcement & Security'), ('Public Transportation', 'Public Transportation'), ('Public Health & Safety', 'Public Health & Safety'), ('Higher Education & Universities', 'Higher Education & Universities'), ('K-12 Schools & Educational Institutions', 'K-12 Schools & Educational Institutions'), ('Research & Development', 'Research & Development'), ('Tech Clubs & Developer Communities', 'Tech Clubs & Developer Communities'), ('Cultural, Arts & Sports Organizations', 'Cultural, Arts & Sports Organizations'), ('Social & Networking Clubs', 'Social & Networking Clubs'), ('Non-Profit & Humanitarian Organizations', 'Non-Profit & Humanitarian Organizations'), ('Environmental & Sustainability', 'Environmental & Sustainability'), ('Startup & Entrepreneurship', 'Startup & Entrepreneurship'), ('IT & Business Consulting', 'IT & Business Consulting'), ('Venture Capital & Investment', 'Venture Capital & Investment'), ('Legal & Compliance Services', 'Legal & Compliance Services'), ('Supply Chain & Logistics', 'Supply Chain & Logistics'), ('Real Estate & Property Management', 'Real Estate & Property Management'), ('Manufacturing & Industrial Technology', 'Manufacturing & Industrial Technology'), ('Agriculture & Food Tech', 'Agriculture & Food Tech'), ('Human Resources & Talent Management', 'Human Resources & Talent Management'), ('Journalism & Publishing', 'Journalism & Publishing'), ('Entertainment & Performing Arts', 'Entertainment & Performing Arts'), ('Religious Organizations', 'Religious Organizations'), ('Hospitality & Tourism', 'Hospitality & Tourism'), ('Other', 'Other')], default='TechClub', max_length=200),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_type',
            field=models.CharField(choices=[('Private', 'Private Company'), ('Open', 'Open Organization'), ('Club Groups', 'Club/Group'), ('Startup', 'Startup'), ('NonProfit', 'Non-Profit Organization'), ('Gov', 'Government Institution'), ('Education', 'Educational Institution'), ('Research Lab', 'Research Lab')], default='Private', max_length=50),
        ),
    ]

# Generated by Django 5.0.3 on 2024-04-25 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_alter_feedback_stars'),
        ('users', '0002_alter_accountant_photo_alter_accountant_resume_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='guest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbaks', to='users.guest'),
        ),
    ]

# Generated by Django 5.0.3 on 2024-05-16 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_alter_feedback_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]
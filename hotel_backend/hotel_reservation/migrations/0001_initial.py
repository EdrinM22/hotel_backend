# Generated by Django 5.0.3 on 2024-03-30 13:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuestInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=100)),
                ('fathers_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('birthplace', models.CharField(blank=True, max_length=100, null=True)),
                ('personal_number', models.CharField(max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], max_length=50, null=True)),
                ('phone_number', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'guest_information',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_unique_number', models.CharField(max_length=100)),
                ('room_name', models.CharField(blank=True, max_length=100, null=True)),
                ('real_price', models.FloatField()),
                ('online_price', models.FloatField()),
                ('description', models.TextField()),
                ('size', models.IntegerField()),
                ('currency', models.CharField(choices=[('usd', 'usd'), ('eur', 'eur'), ('lek', 'lek')], max_length=50)),
            ],
            options={
                'db_table': 'room',
            },
        ),
        migrations.CreateModel(
            name='RoomReservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.CharField(max_length=100)),
                ('total_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'room_type',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('applying_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('paid', models.BooleanField()),
                ('cancelled', models.BooleanField(default=False)),
                ('payment_type', models.CharField(choices=[('online', 'online'), ('reception', 'reception')], max_length=100)),
                ('payment_intent_id', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('total_payment', models.FloatField()),
                ('guest_information', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='hotel_reservation.guestinformation')),
            ],
            options={
                'db_table': 'reservation',
            },
        ),
    ]

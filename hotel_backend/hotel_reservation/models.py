from django.db import models

from users.models import gender_choices, Guest

# Create your models here.
payment_type_choices = (
    ('online', 'online'),
    ('reception', 'reception'),
)

currency_choices = (
    ('usd', 'usd'),
    ('eur', 'eur'),
    ('lek', 'lek'),
)


class GuestInformation(models.Model):
    class Meta:
        db_table = 'guest_information'

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField(blank=True, null=True)
    birthplace = models.CharField(max_length=100, blank=True, null=True)
    personal_number = models.CharField(max_length=100)
    gender = models.CharField(choices=gender_choices, max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Reservation(models.Model):
    class Meta:
        db_table = 'reservation'

    guest_information = models.ForeignKey(GuestInformation, related_name='reservations', on_delete=models.CASCADE,
                                          blank=True, null=True)  # Can be OneToOne think
    guest_user = models.ForeignKey(Guest, related_name='reservations', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    applying_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    paid = models.BooleanField(default=True)
    cancelled = models.BooleanField(default=False)
    payment_type = models.CharField(max_length=100, choices=payment_type_choices, default='eur')
    payment_intent_id = models.CharField(max_length=200, unique=True, blank=True, null=True)
    total_payment = models.FloatField()


class RoomReservation(models.Model):
    reservation = models.ForeignKey(Reservation, related_name='room_reservations', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', related_name='room_reservations', on_delete=models.CASCADE)


class Room(models.Model):
    class Meta:
        db_table = 'room'

    room_unique_number = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100, null=True, blank=True)
    real_price = models.FloatField()
    online_price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    size = models.IntegerField()
    room_type = models.ForeignKey('RoomType', related_name='rooms', on_delete=models.CASCADE)
    currency = models.CharField(max_length=50, choices=currency_choices, default='eur')

    def set_float_price(self):
        self.online_price = float(self.real_price) + 2

    def __str__(self):
        return f'Room: {str(self.room_unique_number)}'


class RoomType(models.Model):
    class Meta:
        db_table = 'room_type'

    type_name = models.CharField(max_length=100, unique=True)
    total_count = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(default=2)

    def __str__(self):
        return str(self.type_name)

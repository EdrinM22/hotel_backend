from rest_framework import serializers

from hotel_reservation.models import Reservation, GuestInformation, Room, RoomReservation

from hotel_reservation.serializers.GuestInformationSerializer import GuestInformationCreateSerializer

from .validators import date_today_serializer


class ReservationAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ('name', 'start_date', 'end_date')


class ReservationCreateViaGuestInfo(ReservationAbstractSerializer):
    room_id = serializers.IntegerField()

    class Meta(ReservationAbstractSerializer.Meta):
        model = Reservation
        fields = ('guest_user', 'payment_type', 'payment_intent_id',
                  'total_payment', 'room_id') + ReservationAbstractSerializer.Meta.fields

    def validate_start_date(self, value):
        return date_today_serializer(value)

    def validate_end_date(self, value):
        return date_today_serializer(value)

    def create(self, validated_data):
        room_id = validated_data.pop('room_id')
        reservation_obj = Reservation.objects.create(**validated_data)
        RoomReservation.objects.create(reservation=reservation_obj, room_id=room_id)
        return reservation_obj


class ReservationCreateViaGuestUser(ReservationAbstractSerializer):
    guest_information = GuestInformationCreateSerializer()
    room_id = serializers.IntegerField()

    class Meta(ReservationAbstractSerializer):
        model = Reservation
        fields = ('guest_information', 'payment_type', 'payment_intent_id', 'total_payment',
                  'room_id') + ReservationAbstractSerializer.Meta.fields

    def validate_start_date(self, value):
        return date_today_serializer(value)

    def validate_end_date(self, value):
        return date_today_serializer(value)

    def create(self, validated_data):
        guest_information = validated_data.pop('guest_information')
        guest_information_obj = GuestInformation.objects.create(**guest_information)
        room_id = validated_data.pop('room_id')
        reservation_obj = Reservation.objects.create(**validated_data, guest_information=guest_information_obj)
        RoomReservation.objects.create(room_id=room_id, reservation=reservation_obj)
        return Reservation

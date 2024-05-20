import datetime

from rest_framework import serializers
from hotel_reservation.models import Room, RoomType, RoomReservation
from .validators import room_name_validator, size_room_type_validator
# from hotel_reservation.serializers.ReservationSerializers import ReservationFilterFromRoomSerializer

class RoomAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('room_unique_number', 'description', 'size')


class RoomCreateManySerializer(RoomAbstractSerializer):
    class Meta(RoomAbstractSerializer.Meta):
        fields = ('real_price', 'room_name', 'room_type', 'currency') + RoomAbstractSerializer.Meta.fields

    def create(self, validated_data):
        if not RoomType.objects.filter(id=validated_data.get('room_type')).exists():
            raise serializers.ValidationError('This Room Type Does Not Exists')
        online_price = validated_data.get('real_price') + 2
        validated_data['online_price'] = online_price
        room_type_obj = RoomType.objects.get(id=validated_data.get('room_type'))
        if not validated_data.get('room_unique_number'):
            validated_data['room_unique_number'] = room_type_obj.type_name + str(online_price)
        if not validated_data.get('size'):
            validated_data['size'] = room_type_obj.size
        room_obj = Room.objects.create(**validated_data)
        return room_obj


class RoomCreateSerializer(RoomAbstractSerializer):
    class Meta(RoomAbstractSerializer.Meta):
        fields = RoomAbstractSerializer.Meta.fields + (
            'real_price', 'room_name', 'room_type', 'currency', 'description', 'online_price')

    # def create(self, validated_data):
    #     online_price = validated_data.get('real_price') + 2
    #     validated_data['online_price'] = online_price
    #     return Room.objects.create(**validated_data)

    # def validate_room_name(self, value):
    #     return room_name_validator(value)


# class RoomReservationListSerializer(serializers.ModelSerializer):
#     reservation = ReservationFilterFromRoomSerializer(read_only=True)
#
#     class Meta:
#         fields = '__all__'
#         model = RoomReservation


class RoomListSerializer(RoomAbstractSerializer):
    # room_reservations = RoomReservationListSerializer(many=True, read_only=True)
    is_reserved = serializers.SerializerMethodField()
    class Meta(RoomAbstractSerializer.Meta):
        fields = ('id', 'real_price', 'online_price', 'room_name', 'room_type', 'currency',
                  'description', 'is_reserved') + RoomAbstractSerializer.Meta.fields

    def get_is_reserved(self, obj: Room):
        date_today = datetime.datetime.now().date()
        return Room.objects.filter(room_reservations__reservation__start_date__lte=date_today,
                                   room_reservations__reservation__end_date__gte=date_today,
                                   pk=obj.pk).exists()




class RoomTypeAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('type_name', 'total_count', 'size')



class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class RoomTypeCreateSerializer(RoomTypeAbstractSerializer):
    # main_image = Base64ImageField(max_length=None, use_url=True)
    class Meta(RoomTypeAbstractSerializer.Meta):
        model = RoomType
        fields = ('type_name', 'total_count', 'size', 'real_price', 'online_price', 'main_image')
        extra_kwargs = {
            'real_price': {'required': True},
            'online_price': {'required': True},
            'main_image': {'required': True},
        }

    def validate_size(self, value):
        return size_room_type_validator(value)


class RoomTypeListSerializer(RoomTypeAbstractSerializer):
    class Meta(RoomTypeAbstractSerializer.Meta):
        fields = ('id', 'real_price', 'online_price', 'main_image') + RoomTypeAbstractSerializer.Meta.fields

class RoomtypeListForScrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('id', 'type_name')

class RoomImagesSerializer(serializers.ModelSerializer):

    class Meta:
        pass


class RoomTypeCustomSerializer(serializers.Serializer):
    room_type = RoomTypeListSerializer(read_only=True)
    room_count = serializers.IntegerField()


class RoomTypeChangePriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomType
        fields = ('online_price', 'real_price')

    def update(self, instance: RoomType, validated_data):
        instance.online_price = validated_data.get('online_price', instance.online_price)
        instance.real_price = validated_data.get('real_price', instance.real_price)
        rooms = instance.rooms.all()
        for room in rooms:
            room.online_price = instance.online_price
            room.real_price = instance.real_price
            room.save()
        instance.save()
        return instance


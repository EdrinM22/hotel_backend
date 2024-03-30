from rest_framework import serializers
from hotel_reservation.models import Room, RoomType
from .validators import room_name_validator, size_room_type_validator


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
    class Meta(RoomAbstractSerializer):
        fields = RoomAbstractSerializer.Meta.fields + (
            'real_price', 'room_name', 'room_type', 'currency', 'description')

    def create(self, validated_data):
        online_price = validated_data.get('real_price') + 2
        validated_data['online_price'] = online_price
        return Room.objects.create(**validated_data)

    def validate_room_name(self, value):
        return room_name_validator(value)


class RoomListSerializer(RoomAbstractSerializer):
    class Meta(RoomAbstractSerializer.Meta):
        fields = ('id', 'real_price', 'room_name', 'room_type', 'currency',
                  'description') + RoomAbstractSerializer.Meta.fields


class RoomTypeAbstractSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = ('type_name', 'total_count', 'size')


class RoomTypeCreateSerializer(RoomTypeAbstractSerializer):
    class Meta(RoomTypeAbstractSerializer.Meta):
        pass

    def validate_size(self, value):
        return size_room_type_validator(value)


class RoomTypeListSerializer(RoomTypeAbstractSerializer):
    class Meta(RoomTypeAbstractSerializer.Meta):
        fields = ('id',) + RoomTypeAbstractSerializer.Meta.fields

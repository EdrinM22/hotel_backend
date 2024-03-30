from rest_framework.serializers import ValidationError


def room_name_validator(value):
    if not value:
        raise ValidationError('room_name is required')
    return value


def size_room_type_validator(value):
    if not value:
        raise ValidationError('Size should not be empty!')
    return value

from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import StatusAdd, Coord, Image, User, LevelPoint


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'full_name',
            'email',
            'phone',
        )


class CoordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coord
        fields = (
            'latitude',
            'longitube',
            'height'
        )


class LevelPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelPoint
        fields = (
            'winter_level',
            'summer_level',
            'spring_level',
            'autumn_level'
        )


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'title',
            'img'
        )


class StatusSerializer(WritableNestedModelSerializer):
    user_id = UserSerializer()
    coord_id = CoordSerializer()
    level = LevelPointSerializer()
    photo = ImageSerializer()

    class Meta:
        model = StatusAdd
        fields = (
            'glory_title',
            'title',
            'other_titles',
            'connect',
            'date',
            'coord_id',
            'user_id',
            'photo',
            'status',
            'level'
        )

    def validate(self, data):
        if self.instance is not None:
            if self.instance.status != 'NW':
                raise serializers.ValidationError(
                    f'Отказ! Причина: статус{self.instance.get_status_display()}'
                )
        user = self.instance.user_id
        user_data = data.get('user_id')
        user_fields = [
            user.full_name != user_data['full_name'],
            user.email != user_data['email'],
            user.phone != user_data['phone'],
        ]

        if user_data is not None and any(user_fields):
            raise serializers.ValidationError(
                f'Отклонено! Нельзя менять данные пользователя'
            )
        return data

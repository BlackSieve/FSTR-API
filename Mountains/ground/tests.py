"""
Описание тестов для StatusAddTest:

1.setUp:
-Метод выполняется перед каждым тестом и создает необходимые объекты для тестирования.

2.test_create_status_add:
-Тест создает объект 'StatusAdd' и проверяет, что все поля установлены корректно.

3.test_title_unique_constraint:
-Проверяет уникальность поля 'title'.
PS. Если попытаться создать две записи с одинаковыми значениями, должно возникнуть исключение

4.test_other_titles_unique_constraint:
- Проверяет уникальность поля `other_titles`.

5.test_status_choices:
- Проверяет установку и изменение статуса. Убедитесь, что статус можно установить в любое из определенных значений.

6.test_data_auto_now_add:
- Проверяет, что поле `date` автоматически устанавливается при создании объекта.

Описание тестов для StatusAddSerializerTest:

1. setUp:
- Метод выполняется перед каждым тестом и создает необходимые объекты в базе данных, которые будут использоваться в
 последующих тестах. Здесь мы создаем экземпляры классов `Coord`, `Users`, `Image`, `LevelPoint` и `StatusAdd`.
 Это позволяет избежать повторения кода в каждом тесте, так как нам нужно будет использовать эти объекты.

2. test_serializer_creates_status_add:
- Проверить, что сериализатор корректно создает объект `StatusAdd`.

3. test_serializer_update_status_add:
- Проверить, что сериализатор корректно обновляет существующий объект `StatusAdd`.

4. test_serializer_update_with_invalid_status:
- Проверить, что сериализатор вызывает ошибку валидации при попытке обновить объект с недопустимым статусом.

5. test_invalid_user_data_change:
- Проверить, что изменение данных пользователя вызывает ошибку валидации.

"""

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from .models import LevelPoint, Coord, User, StatusAdd, Image
from .serializers import StatusSerializer


class StatusAddTest(TestCase):
    def setUp(self):
        self.coord = Coord.objects.create(latitude=5.8000000, longitude=5.400000, height=10)
        self.user = User.objects.create(full_name='Иванов Иван Иванович', email='e@example.com', phone='89999999999')
        self.image = Image.objects.create(title='эльбрус', img='http://127.0.0.1:8000/70586_GRYZeHJ.jpg')
        self.level_point = LevelPoint.objects.create(winter_level='1A', spring_level='1A', summer_level='1A',
                                                     autumn_level='1A')

    def test_create_status_add(self):
        status = StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )

        self.assertIsInstance(status, StatusAdd)
        self.assertEqual(status.beauty_title, 'Пик Эльбруса')
        self.assertEqual(status.title, 'Эльбрус')
        self.assertEqual(status.other_titles, 'Летом не сложно добраться')
        self.assertEqual(status.connect, 'Остальное:')
        self.assertEqual(status.coord_id, self.coord)
        self.assertEqual(status.user_id, self.user)
        self.assertEqual(status.photo, self.image)
        self.assertEqual(status.level, self.level_point)
        self.assertEqual(status.status, StatusAdd.NEW)

    def test_title_unique_constraint(self):
        StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )

        with self.assertRaises(Exception):
            StatusAdd.objects.create(
                beauty_title='Пик Эльбруса2',
                title='Эльбрус',
                other_titles='Другое описание',
                connect='Другое остальное',
                coord_id=self.coord,
                user_id=self.user,
                photo=self.image,
                level=self.level_point
            )

    def test_other_titles_unique_constraint(self):
        StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )
        with self.assertRaises(Exception):
            StatusAdd.objects.create(
                beauty_title='Пик Эльбруса-3',
                title='Другой Эльбрус',
                other_titles='Летом не сложно добраться',
                connect='Другое остальное:',
                coord_id=self.coord,
                user_id=self.user,
                photo=self.image,
                level=self.level_point
            )

    def test_status_choices(self):
        status = StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )
        status.status = StatusAdd.ACCEPTED
        status.save()
        self.assertEqual(status.status, StatusAdd.ACCEPTED)

    def test_data_auto_now_add(self):
        status = StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )
        self.assertIsNotNone(status.date)


class StatusAddSerializerTest(APITestCase):
    def setUp(self):
        self.coord = Coord.objects.create(latitude=5.8000000, longitude=5.400000, height=10)
        self.user = User.objects.create(full_name='Иванов Иван Иванович', email='e@example.com', phone='89999999999')
        self.image = Image.objects.create(title='эльбрус', img='http://127.0.0.1:8000/70586_GRYZeHJ.jpg')
        self.level_point = LevelPoint.objects.create(winter_level='1A', spring_level='1A', summer_level='1A',
                                                     autumn_level='1A')
        self.status = StatusAdd.objects.create(
            beauty_title='Пик Эльбруса',
            title='Эльбрус',
            other_titles='Летом не сложно добраться',
            connect='Остальное:',
            coord_id=self.coord,
            user_id=self.user,
            photo=self.image,
            level=self.level_point
        )

    def test_serializer_creates_status_add(self):
        data = {
            'beauty_title': 'Пик Эльбруса',
            'title': 'Эльбрус',
            'other_titles': 'Летом не сложно добраться',
            'connect': 'Остальное:',
            'coord_id': {'latitude': '5.80000000', 'longitude': '5.40000000', 'height': 10},
            'user_id': {'full_name': 'Иванов Иван Иванович', 'email': 'e@example.com', 'phone': '89999999999'},
            'level': {'winter_level': '1A', 'spring_level': '1A', 'summer_level': '1A', 'autumn_level': '1A'},
            'photo_img': {'title': 'эльбрус', 'img': 'http://127.0.0.1:8000/70586_GRYZeHJ.jpg'},
            'status': 'NW',
        }
        serializer = StatusSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        status = serializer.save()
        self.assertIsNotNone(status.id)

    def test_serializer_update_status_add(self):
        data = {
            'beauty_title': 'Пик Эльбруса',
            'title': 'Эльбрус',
            'other_titles': 'Летом не сложно добраться',
            'connect': 'Остальное:',
            'coord_id': {'latitude': '5.80000000', 'longitude': '5.40000000', 'height': 10},
            'user_id': {'full_name': 'Иванов Иван Иванович', 'email': 'e@example.com', 'phone': '89999999999'},
            'level': {'winter_level': '1A', 'spring_level': '1A', 'summer_level': '1A', 'autumn_level': '1A'},
            'photo_img': {'title': 'эльбрус', 'img': 'http://127.0.0.1:8000/70586_GRYZeHJ.jpg'},
            'status': 'NW',
        }
        serializer = StatusSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        updated_status = serializer.save()
        self.assertEqual(updated_status.beauty_title, 'Пик Эльбруса')

    def test_serializer_update_with_invalid_status(self):
        self.status.status = 'AC'
        self.status.save()
        data = {
            'beauty_title': 'Пик Эльбруса',
            'title': 'Эльбрус',
            'other_titles': 'Летом не сложно добраться',
            'connect': 'Остальное:',
            'coord_id': {'latitude': '5.80000000', 'longitude': '5.40000000', 'height': 10},
            'user_id': {'full_name': 'Иванов Иван Иванович', 'email': 'e@example.com', 'phone': '89999999999'},
            'level': {'winter_level': '1A', 'spring_level': '1A', 'summer_level': '1A', 'autumn_level': '1A'},
            'photo_img': {'title': 'эльбрус', 'img': 'http://127.0.0.1:8000/70586_GRYZeHJ.jpg'}}

        serializer = StatusSerializer(instance=self.status, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_user_data_change(self):
        data = {
            'beauty_title': 'Пик Эльбруса',
            'title': 'Эльбрус',
            'other_titles': 'Летом не сложно добраться',
            'connect': 'Остальное:',
            'coord_id': {'latitude': '5.80000000', 'longitude': '5.40000000', 'height': 10},
            'user_id': {'full_name': 'Иванов Иван Иванович', 'email': 'e@example.com', 'phone': '89999999999'},
            'level': {'winter_level': '1A', 'spring_level': '1A', 'summer_level': '1A', 'autumn_level': '1A'},
            'photo_img': {'title': 'эльбрус', 'img': 'http://127.0.0.1:8000/70586_GRYZeHJ.jpg'}}

        serializer = StatusSerializer(instance=self.status, data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

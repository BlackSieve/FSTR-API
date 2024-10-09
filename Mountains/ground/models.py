from django.db import models


class User(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=20, unique=True)


class Coord(models.Model):
    latitude = models.DecimalField(max_length=10, decimal_places=8, unique=True)
    longitube = models.DecimalField(max_length=10, decimal_places=8, unique=True)
    height = models.IntegerField(unique=True)


class Image(models.Model):
    title = models.CharField(max_length=200)
    img = models.ImageField()


class LevelPoint(models.Model):
    LEVEL_1A = '1А'
    LEVEL_1B = '1Б'
    LEVEL_2A = '1А'
    LEVEL_2B = '1Б'
    LEVEL_3A = '1А'
    LEVEL_3B = '1Б'

    LEVEL_CHOICES = (
        ('1A', '1A'),
        ('1Б', '1Б'),
        ('2А', '2Б'),
        ('2А', '2Б'),
        ('3А', '3Б'),
        ('3Б', '3Б'),
    )

    winter_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    summer_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    spring_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)
    autumn_level = models.CharField(max_length=2, choices=LEVEL_CHOICES, default=LEVEL_1A)


class StatusAdd(models.Model):
    NEW = 'NW'
    ACCEPTED = 'AC'
    PENDING = 'PD'
    REJECTED = 'RJ'

    STATUS_CHOICES = (
        ('NW', 'NEW'),
        ('AC', 'ACCEPTED'),
        ('PD', 'PENDING'),
        ('RJ', 'REJECTED')
    )

    glory_title = models.CharField(max_length=200)
    title = models.CharField(max_length=200, unique=True)
    other_titles = models.CharField(max_length=300, unique=True)
    connect = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    coord_id = models.OneToOneField(Coord, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.OneToOneField(Image, on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES, default=NEW)
    level = models.ForeignKey(LevelPoint, on_delete=models.CASCADE)

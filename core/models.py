from django.contrib.auth import models as auth

from django.db import models

# Create your models here.


class User(auth.AbstractBaseUser):
    USERNAME_FIELD = 'username'

    username = models.CharField(
        max_length=20,
        unique=True,
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Category(models.Model):
    name = models.CharField(max_length=48)
    board_parameter = models.CharField(max_length=24)

    class Meta:
        db_table = 'categories'


class Article(models.Model):
    category = models.ForeignKey(
        'core.Category',
        on_delete=models.CASCADE,
        related_name='articles'
    )

    title = models.CharField(max_length=128)
    body = models.TextField()
    date = models.DateTimeField()
    url = models.URLField()

    class Meta:
        db_table = 'articles'
        unique_together = ('title', 'date', )


class Doc2VecModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    epochs = models.IntegerField(default=0)
    instance = models.BinaryField()

    class Meta:
        db_table = 'doc2vec_models'

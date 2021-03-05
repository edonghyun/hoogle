import pickle

from django.contrib.auth import models as auth
from django.db.models.query import QuerySet
from django.db import models


class User(auth.AbstractBaseUser):
    USERNAME_FIELD = 'username'

    username = models.CharField(
        max_length=20,
        unique=True,
    )
    objects = auth.BaseUserManager()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'users'


class Category(models.Model):
    name = models.CharField(max_length=48)
    board_parameter = models.CharField(max_length=24)

    class Meta:
        db_table = 'categories'


class Article(models.Model):
    weight = 0

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
    _instance = models.FileField()

    @property
    def instance(self):
        instance = self._instance
        if not instance:
            return None
        return pickle.load(
            instance
        )

    def get_most_similar(self, tokenized_query=None, topn=None):
        model = self.instance
        model.random.seed(0)
        infer_vector = model.infer_vector(tokenized_query)
        return model.docvecs.most_similar(
            positive=[infer_vector],
            topn=topn
        )

    class Meta:
        db_table = 'doc2vec_models'

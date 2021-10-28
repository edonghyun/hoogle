from rest_framework.serializers import ModelSerializer

from core.models import Article


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article

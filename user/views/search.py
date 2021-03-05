from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from django.utils.timezone import now
from django.shortcuts import render
from core.models import Article, Doc2VecModel
from .base import BaseListView


def get_weighted_queryset(queryset=[], query='', doc2vec_model=None):
    # query preprocess
    query = [
        word_tokenize(word) for word in [query.lower()]
    ].pop()

    query = [
        token for token in query
        if token not in stopwords.words('english')
    ]

    # Idf = db.select_idf_values(removed_stopwords_query)

    # 토큰 수 두 개 이하의 쿼리는 유저 관심도 및 텀프리퀀시 중심으로 가중치 반영
    if len(query) > 2:
        WEIGHT_SIMILARITY = 4.0
        WEIGHT_LATEST = 1.0
        WEIGHT_CATEGORY = 0.3
        WEIGHT_USER_INTEREST = 0.4
        WEIGHT_TERM_FREQUENCY = 0.3
        WEIGHT_ADDNEWEST = 1.0
        WEIGHT_IDF = 1.0
    else:
        WEIGHT_SIMILARITY = 2.4
        WEIGHT_LATEST = 1.0
        WEIGHT_CATEGORY = 0.1
        WEIGHT_USER_INTEREST = 2.0
        WEIGHT_TERM_FREQUENCY = 1.6
        WEIGHT_ADDNEWEST = 1.0
        WEIGHT_IDF = 1.0

    weighted_articles = list()
    similar_articles = doc2vec_model.get_most_similar(
        tokenized_query=query,
        topn=100,
    )

    for url, similarity in similar_articles:
        try:
            article = queryset.get(url=url)
            article.weight = similarity * WEIGHT_SIMILARITY
            weighted_articles.append(article)
        except:
            continue

    # Engine.addWeightCategory(news_and_weight, str_query, WEIGHT_CATEGORY)
    for article in weighted_articles:
        time_delta = (article.date - now()).days * WEIGHT_LATEST * 0.0005
        article.weight -= time_delta

    stopwrds = stopwords.words('english')
    for terms in query:
        for article in weighted_articles:
            count = article.title.count(terms) \
                + article.body.count(terms)
            article.weight += count * WEIGHT_TERM_FREQUENCY

    # Engine.addWeightIDF(
    #     news_and_weight, removed_stopwords_query, WEIGHT_IDF, Idf
    # )
    weighted_articles.sort(key=lambda x: x.weight, reverse=True)
    return weighted_articles


class SearchListView(BaseListView):
    model = Article
    template_name = 'index.html'

    @property
    def doc2vec_model(self):
        return Doc2VecModel.objects.last()

    def get_queryset(self):
        query = self.request.GET.get('query')
        if not query:
            return []

        queryset = super().get_queryset()
        return get_weighted_queryset(
            queryset=queryset,
            query=query,
            doc2vec_model=self.doc2vec_model,
        )

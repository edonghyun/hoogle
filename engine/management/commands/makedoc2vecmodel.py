import time

from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from stop_words import get_stop_words
from nltk.tokenize import word_tokenize

import pickle
import pandas as pd
import multiprocessing
import re
import warnings
import logging

from core.models import (
    Article,
    Doc2VecModel,
)

from django.core.management import BaseCommand
from django.db import transaction


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-e',
            '--epochs',
            dest='epochs',
            default=20,
        )
        parser.add_argument(
            '-s',
            '--size',
            dest='size',
            default=100,
        )
        parser.add_argument(
            '-s',
            '--window',
            dest='window',
            default=5,
        )
        parser.add_argument(
            '-s',
            '--alpha',
            dest='alpha',
            default=0.025,
        )
        parser.add_argument(
            '-s',
            '--min_alpha',
            dest='min_alpha',
            default=0.025,
        )

    def handle(self, **options):
        self.epochs = options['epochs']
        self.size = options['size']
        self.window = options['window']
        self.alpha = options['alpha']
        self.min_alpha = options['min_alpha']

        logger.info('start make doc2vec model')
        self.make_model()
        logger.info('making doc2vec model ended')

    def make_model(self):
        docs = []
        start = time.clock()
        articles = Article.objects.all()
        for article in articles:
            id = article.url
            text = re.sub(
                '[!"#%\'()*+,/:;<=>?\[\]\\xa0^_`{|}~’”“′‘\\\]', ' ', article.title.lower())
            text += " " + article.body.lower()
            text = word_tokenize(text)
            T = TaggedDocument(text, [id])
            docs.append(T)
        end1 = time.clock()

        logger.info(f'text preprocessing processed in {end1-start}')

        # initialize a model
        model = Doc2Vec(
            size=self.size,
            window=self.window,
            alpha=self.alpha,
            min_alpha=self.min_alpha,
            min_count=0,
            dm=0,
            workers=multiprocessing.cpu_count()
        )

        # build vocabulary
        model.build_vocab(docs)
        end2 = time.clock()

        logger.info(f'doc2vec model is made in {end2-end1}')

        # train model
        model.train(docs, total_examples=len(docs), epochs=self.epochs)
        end3 = time.clock()

        logger.info(f'epochs {self.epochs} times: {end3-end2}')

        # save model
        Doc2VecModel.objects.create(
            epochs=self.epochs,
            instance=pickle.dumps(
                model
            )
        )

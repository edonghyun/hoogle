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


from django.core.files.base import ContentFile

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
            '--vector_size',
            dest='vector_size',
            default=100,
        )
        parser.add_argument(
            '-w',
            '--window',
            dest='window',
            default=5,
        )
        parser.add_argument(
            '-a',
            '--alpha',
            dest='alpha',
            default=0.025,
        )
        parser.add_argument(
            '-ma',
            '--min_alpha',
            dest='min_alpha',
            default=0.025,
        )
        parser.add_argument(
            '-mc',
            '--min_count',
            dest='min_count',
            default=1,
        )

    def handle(self, **options):
        self.epochs = options['epochs']
        self.vector_size = options['vector_size']
        self.window = options['window']
        self.alpha = options['alpha']
        self.min_alpha = options['min_alpha']
        self.min_count = options['min_count']

        logger.info('start make doc2vec model')
        self.make_model()
        logger.info('making doc2vec model ended')

    def make_model(self):
        def get_text(article):
            text = re.sub(
                '[!"#%\'()*+,/:;<=>?\[\]\\xa0^_`{|}~’”“′‘\\\]', ' ', article.title.lower()
            )
            return f'{text} {article.body.lower()}'

        start_at = time.clock()
        docs = [
            TaggedDocument(
                words=word_tokenize(
                    get_text(
                        article
                    )
                ),
                tags=[article.url]
            ) for article in Article.objects.all()
        ]
        end_at_1 = time.clock()

        logger.info(f'text preprocessing processed in {end_at_1-start_at}')

        # initialize a model
        model = Doc2Vec(
            vector_size=self.vector_size,
            window=self.window,
            alpha=self.alpha,
            min_alpha=self.min_alpha,
            min_count=self.min_count,
            workers=multiprocessing.cpu_count()
        )

        # build vocabulary
        model.build_vocab(docs)
        end_at_2 = time.clock()

        logger.info(f'doc2vec model is made in {end_at_2-end_at_1}')

        # train model
        model.train(docs, total_examples=len(docs), epochs=self.epochs)
        end_at_3 = time.clock()

        logger.info(f'epochs {self.epochs} times: {end_at_3-end_at_2}')

        # save model
        doc2vec_model_instance = Doc2VecModel.objects.create(
            epochs=self.epochs,
        )

        model_data = pickle.dumps(model)
        f = ContentFile(model_data)
        doc2vec_model_instance._instance.save('test', f)
        f.close()

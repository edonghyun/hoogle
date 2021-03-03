import logging

from django.core.management import BaseCommand
from django.db import transaction

from core.models import Category

logger = logging.getLogger(__name__)

categories = [
    {
        'name': 'National',
        'board_parameter': '020100000000',
    },
    {
        'name': 'Business',
        'board_parameter': '020200000000',
    },
    {
        'name': 'Finance',
        'board_parameter': '021900000000',
    },
    {
        'name': 'Life&Style',
        'board_parameter': '020300000000',
    },
    {
        'name': 'Entertainment',
        'board_parameter': '020400000000',
    },
    {
        'name': 'Sport',
        'board_parameter': '020500000000',
    },
    {
        'name': 'World',
        'board_parameter': '021200000000',
    },
    {
        'name': 'Opinion',
        'board_parameter': '020600000000',
    },
]


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, **options):
        logger.info('start seeding forum boards ....')
        for category in categories:
            logger.info('creating forum board {0[name]}'.format(category))
            Category.objects.create(**category)
        logger.info('done seeding forum boards')

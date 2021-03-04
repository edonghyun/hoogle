import logging
import requests
import collections

from datetime import datetime
from urllib.parse import parse_qs, urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


from django.core.management import BaseCommand
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_date


from core.models import (
    Category,
    Article,
)

logger = logging.getLogger(__name__)

MAX_PAGE = 10000


class Command(BaseCommand):
    base_page_url = 'http://www.koreaherald.com/list.php?ct={0}'
    base_detail_page_url = 'http://www.koreaherald.com/'
    detail_urls = []

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--start-date',
            dest='start_date',
            required=False,
        )
        parser.add_argument(
            '-e',
            '--end-date',
            dest='end_date',
            required=False,
        )
        parser.add_argument(
            '-r',
            '--recent-date',
            dest='parse_recent_posts',
            default=False,
        )
        parser.add_argument(
            '-t',
            '--threads',
            type=int,
            default=1,
            dest='num_threads'
        )

    def handle(self, **options):
        self.num_threads = options['num_threads']

        categories = Category.objects.all()
        detail_urls = collections.defaultdict(list)
        for category in categories:
            url = self.base_page_url.format(category.board_parameter)
            last_page = self.parse_last_page(url)

            added_url_number = 0
            for page in range(last_page):
                list_url = url + f'&np={page}'
                urls = self.parse_list(list_url)
                detail_urls[category.name] += urls
                added_url_number += len(urls)
                if added_url_number >= MAX_PAGE:
                    break
            logger.info(f'{category.name} {added_url_number} added ...')
        logger.info(f'{len(detail_urls)} articles parsing started')

        def parse(category_name, url):
            try:
                title, body, date = self.parse_detail(url)
                category = Category.objects.get(
                    name=category_name,
                )
                article = Article.objects.create(
                    category=category,
                    title=title,
                    body=body,
                    date=parse_date(date),
                )
            except django.db.utils.IntegrityError:
                pass
            except Exception as exc:
                logger.error(exc, exc_info=True)

        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            logger.info(f'parse {len(detail_urls)} articles')
            for category_name, urls in detail_urls.items():
                for url in urls:
                    url = urljoin(
                        self.base_detail_page_url, url)
                    executor.submit(parse, category_name, url)
        logger.info(f'article parsing ended')

    def get_beautifulsoup(self, url):
        headers = {
            'user-agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                'AppleWebKit/537.36 (KHTML, like Gecko)'
                'Chrome/75.0.3770.142 Safari/537.36'
            )
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def parse_last_page(self, url):
        soup = self.get_beautifulsoup(url)
        last_page_element = soup.select('ul.paging li')[-1]
        last_page_url = last_page_element.find('a')['href']
        query_string = parse_qs(last_page_url)
        return int(query_string.get('np')[0])

    def parse_detail(self, url):
        soup = self.get_beautifulsoup(url)
        title = soup.select_one('h1.view_tit').get_text()
        body = ' '.join([
            b.get_text() for b in soup.select('div.view_con_t')
        ])

        date = soup.select_one(
            'div.view_tit_byline_r').get_text().split(' ')[2:5]
        day = int(date[1].split(',')[0])
        month = datetime.strptime(date[0], '%b').month
        date = f'{date[2]}-{day:02}-{month:02}'
        return (title, body, date, )

    def parse_list(self, url):
        soup = self.get_beautifulsoup(url)
        a_tags = soup.select('div.main_sec a')
        return [
            a['href'] for a in a_tags
        ]

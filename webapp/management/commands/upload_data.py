from django.core.management.base import BaseCommand
from django.conf                 import settings
from os.path                     import exists
from yaml                        import dump, load

from webapp.utils                import _to_date, _clean_text
from webapp.models               import FoodReviews

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='path to txt file')
        parser.add_argument('--limit', type=int, help='to limit no of data upload')

    def handle(self, *args, **kwargs):
        rawfile    = kwargs['file_path']
        limit      = kwargs['limit']
        index_data = {}

        with open(rawfile, encoding='latin-1') as f:
            _data = {}
            total = 0
            for line in f.readlines():
                if not line.strip() == '':
                    try:
                        key, value = line.strip().split(':', 1)
                        _data[key] = value
                    except: pass
                else:
                    # trimming and striping values.
                    _data = dict([(k, v.strip()) for k, v in _data.items()])

                    # Inserting data to db from txt file.
                    obj = FoodReviews.objects.create(
                        product_id  = _data.get('product/productId'),
                        user_id     = _data.get('review/userId'),
                        name        = _data.get('review/profileName'),
                        helpfulness = _data.get('review/helpfulness'),
                        score       = _data.get('review/score'),
                        timestamp   = _to_date(int(_data.get('review/time'))),
                        summary     = _data.get('review/summary'),
                        text        = _data.get('review/text'))

                    # Creating inverted index for storing data (field - text)
                    _text = _clean_text(obj.text)
                    for k, v in _text.items():
                        index_data.setdefault(k.lower(), []).append({'pk': obj.pk, 'count': v})

                    total += 1
                    print('\r{} records inserted and indexed'.format(total), end='')
                    _data = {}

                    if limit and total >= limit:
                        break

            # writing inverted index to YAML file.
            with open(settings.INV_INDEX, 'w') as f:
                dump(index_data, f, default_flow_style=False)

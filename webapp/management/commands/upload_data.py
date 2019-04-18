from django.core.management.base import BaseCommand
from django.conf                 import settings
from collections                 import Counter
from datetime                    import datetime
from os.path                     import exists
from string                      import punctuation
from yaml                        import dump, load

from webapp.models               import FoodReviews

# Helper functions
def _to_date(d):
    return datetime.fromtimestamp(d) if d else None

def _clean_text(text):
    text = text.lower()
    stop_words = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
                   "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
                   "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
                   "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
                   "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him",
                   "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in",
                   "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my",
                   "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours",
                   "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should",
                   "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
                   "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll",
                   "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up",
                   "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when",
                   "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
                   "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
                   "yourselves"]

    text = text.translate(text.maketrans('', '', punctuation))
    text = [x.strip() for x in text.split(' ') if x and x not in stop_words]
    return Counter(text)

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

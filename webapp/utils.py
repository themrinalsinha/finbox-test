from django.conf import settings

from collections import Counter
from datetime    import datetime
from string      import punctuation
from yaml        import load, Loader

STOP_WORDS = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
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

def _to_date(d):
    return datetime.fromtimestamp(d) if d else None

def _clean_text(text):
    text = text.lower()
    text = text.translate(text.maketrans('', '', punctuation))
    text = [x.strip() for x in text.split(' ') if x and x not in STOP_WORDS]
    return Counter(text)

class FinboxSearch(object):
    def __init__(self, text):
        self.text  = text
        self.index = load(open(settings.INV_INDEX), Loader=Loader)

    def get_value(self, key):
        return self.index.get(key, [])

    def _text_to_token(self):
        return [x for x in self.text.split(' ') if x not in STOP_WORDS]

    def _token_data(self):
        tokens = self._text_to_token()
        return dict(zip(tokens, [self.get_value(x) for x in tokens]))

    def _calculate_score(self):
        counter = {}
        data    = self._token_data()
        doc_ids = [[a.get('pk') for a in y] for x, y in data.items()]

        intersections = []
        for i in range(len(doc_ids)):
            _res = set(doc_ids[i])
            for j in range(i, len(doc_ids)):
                if doc_ids[i] == doc_ids[j]:
                    continue
                _intersections = _res.intersection(doc_ids[j])
                if _intersections:
                    intersections.extend(list(_intersections))

        # Here incrementing counter value by 1 (as 1 is by default)
        common_docs = dict([(x, y+1) for x, y in Counter(intersections).items()])

        # Now calculate and put score for the documents
        calc_score  = lambda *x: (sum(x)/len(data))
        for key, value in data.items():
            for _val in value:
                if _val.get('pk') not in common_docs:
                    _val.setdefault('score', calc_score(1))
                else:
                    _val.setdefault('score', calc_score(common_docs.get(_val.get('pk'))))

        return data

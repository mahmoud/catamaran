import itertools
from collections import defaultdict

'''
>>> category_overlaps.article_category_dict2category_set_counts(
{'cats':['mammals', 'felines', 'pets'], 'dogs':['mammals', 'canines', 'pets'],
'goldfish':['fish', 'pets']})

defaultdict(<type 'int'>, {('mammals', 'felines', 'pets'): 1,
('fish', 'pets'): 1, ('pets',): 3, ('mammals', 'pets'): 2, ('mammals',): 2,
('fish',): 1, ('felines', 'pets'): 1, ('canines',): 1,
('mammals', 'canines', 'pets'): 1, ('mammals', 'felines'): 1, ('felines',): 1,
('canines', 'pets'): 1, ('mammals', 'canines'):1})
'''

def article_category_dict2category_set_counts(article_category_dict):
    category_set_counts = defaultdict(int)
    for category_list in article_category_dict.values():
        for i in range(len(category_list)):
            for subset in itertools.combinations(category_list, i+1):
                category_set_counts[subset] += 1
    return category_set_counts

class Recommendation(object):
    def __init__(self, confidence, category, reason):
        self.confidence = confidence
        self.category   = category
        self.reason     = reason

def make_recommendations(category_list, category_set_counts):
    '''
    Given that an item is in the given list of categories, give recommendations
    for other categories it is probably in.
    
    Takes the output of compact as an input.
    
    Returns a list of CategoryRecommendation objects.
    '''
    subset = frozenset(category_list)
    results = {}
    for k in category_set_counts:
        if not k.isdisjoint(subset):
            #note, overlaps can happen -- have maximum confidence overwrite
            overlap = subset & k
            confidence = 1.0 * category_set_counts[k] / category_set_counts[k&subset]
            for category in overlap:
                if confidence > results.get(category, 0):
                    results[category] = Recommendation(
                        confidence = confidence,
                        reason     = overlap,
                        category   = category
                    )
    return sorted(results.values(), key=lambda a: a.confidence)

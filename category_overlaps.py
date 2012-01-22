import collections

def process_overlaps(category_article_dict, depth=2):
    '''
    figures out how much categories overlap
    input:
    category_article_dict = {category id : iterable of article ids}
    depth = how large sets to build
    
    output:
    [{set of one category   id : set of article ids in category},
     {set of two category   ids: set of article ids in both categories},
     {set of three category ids: set of article ids in all three categories]}
     ...
    ]
    
    O(n) behavior is depth * n**2
    
    >>> category_overlaps.process_overlaps({"a":[1,2,3], "b":[1,2], "c":[3,4,5]})
[{frozenset(['c']): [3, 4, 5], frozenset(['b']): [1, 2], frozenset(['a']): [1, 2
, 3]}, {}]
    '''
    category_article_set_dict = dict([(c, set(category_article_dict[c]))
                                        for c in category_article_dict])
    sofar = [dict([(frozenset(c), set(category_article_dict[c]))
                        for c in category_article_dict])]
    return _process_overlaps2(category_article_set_dict, depth-1, sofar)

def _process_overlaps2(cat_dict, depth, sofar):
    'recursive helper for process_overlaps'
    if depth == 0:
        return sofar
    
    prev = sofar[-1]
    next = {}
        
    for left_category in cat_dict:
        left = cat_dict[left_category]
        for right_category_set in prev:
            if left_category not in right_category_set:
                right  = prev[right_category_set]
                #union of key sets
                newkey = frozenset([left_category]) | right_category_set
                #intersection of value sets
                newval = left & right
                if len(newval) > 0: #the vast majority of overlaps will be empty
                    next[newkey] = newval
            
    return _process_overlaps2(cat_dict, depth-1, sofar+[next])
            


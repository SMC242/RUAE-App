from json import dump
from typing import List, Dict

# modify this dict
# format = aliases : info
toSend: Dict[str , str] = {
    "u, understanding" : '''    Strategy: Summarise in your own words.
    Keywords: "own words", "summarise", "points".
    Marks: 1 per point.''',

    "a, analysis" : '''    Strategy : Quote, technique, connotations, effects.
    Keywords: "close reference", "show", "language".
    Marks: 1 for brief, 2 for 2 large points.
    Tip: go for 1 mark most of the time.''',

    "e, evaluation" : '''    Strategy: State why the target is good/bad,
    quote, give brief analysis, repeat once.
    Keywords: synonyms of "how well"/"how badly".
    Marks: 2-3
    Tip: agree with the question.'''
}

#write to file
with open("skills.json", "w") as f:
    json = dump(toSend, f)

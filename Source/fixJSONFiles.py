from json import dump

with open("settings.json", "w") as f:
    toDump = {"dark" : "True"}
    dump(toDump, f)

with open("skills.json", "w") as f:
    toDump = {
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
    dump(toDump, f)

input("Files reset to default settings. Press any key to exit")
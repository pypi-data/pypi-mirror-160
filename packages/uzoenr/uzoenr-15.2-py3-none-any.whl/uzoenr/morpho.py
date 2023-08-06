import pymorphy2
morph = pymorphy2.MorphAnalyzer()

def morphology(word):
    p = morph.parse(word)
    return [[i.word for i in mor.lexeme] for mor in p][0]

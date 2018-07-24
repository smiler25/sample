"""
Классификатор фраз
Правило принадлежности запроса теме:
1. Если набор слов из запроса содержит в себе все слова какой-либо из фраз,
   то запрос считается соответствующим теме (да). Иначе - не соответствующим (нет).
2. Порядок слов в запросе и во фразах не учитывается.

"""


from collections import defaultdict


class Classifier:
    def __init__(self, phrases):
        self.phrases = phrases
        self.words_count = [len(o.split()) for o in phrases]
        self.words_phrases = defaultdict(list)
        for i, phrase in enumerate(phrases):
            for word in set(phrase.split()):
                self.words_phrases[word].append(i)

    def __call__(self, phrase):
        words = set(phrase.split())
        if not words:
            return False
        phrases = {}
        for word in words:
            used_in = self.words_phrases.get(word)
            if not used_in:
                continue
            for phrase_index in used_in:
                left = phrases.get(phrase_index)
                if left is None:
                    left = self.words_count[phrase_index] - 1
                else:
                    left -= 1
                if not left:
                    return True
                phrases[phrase_index] = left
        return False

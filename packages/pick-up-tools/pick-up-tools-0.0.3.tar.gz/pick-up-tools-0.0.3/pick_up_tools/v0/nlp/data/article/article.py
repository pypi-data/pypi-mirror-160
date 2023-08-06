from v0.nlp.tools import object_uuid
from v0.nlp.tools.cut import cut_sentence_loose
from v0.nlp.algorithm.sentiment import sentiment_score


class Text(object):
    def __init__(self, text, index=None):
        self.index = index
        self.uuid = object_uuid(text)
        self.text = text

        self._word = None
        self._keyword = None
        self._sentiment = None

    @property
    def word(self):
        if self._word is None:
            self._word = ''
        return self._word

    @property
    def keyword(self):
        if self._keyword is None:
            self._keyword = ''
        return self._keyword

    @property
    def sentiments(self):
        if self._sentiment is None:
            self._sentiment = sentiment_score(self.text)
        return self._sentiment


class Article(Text):
    def __init__(self, text):
        super(Article, self).__init__(text)
        self._sentence = None

    @property
    def sentence(self):
        if self._sentence is None:
            _sentence = cut_sentence_loose(self.text)
            self._sentence = [Sentence(i) for i in _sentence]
        return self._sentence


class Sentence(Text):
    ...


if __name__ == '__main__':
    ...

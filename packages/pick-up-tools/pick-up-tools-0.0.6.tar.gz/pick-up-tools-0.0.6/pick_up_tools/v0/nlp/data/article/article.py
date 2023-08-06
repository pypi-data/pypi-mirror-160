from pick_up_tools.v0.nlp.tools import object_uuid
from pick_up_tools.v0.nlp.tools.cut import cut_sentence_loose
from pick_up_tools.v0.nlp.algorithm.sentiment import sentiment_score


class Text(object):
    def __init__(self, text, index=None):
        self.index = index
        self.uuid = object_uuid(text)
        self.text = text

        self._word = None
        self._keyword = None
        self._sentiment = None

    @property
    def word(self) -> list:
        if self._word is None:
            self._word = []
        return self._word

    @property
    def keyword(self) -> list:
        if self._keyword is None:
            self._keyword = []
        return self._keyword

    @property
    def sentiments(self) -> float:
        if self._sentiment is None:
            self._sentiment = sentiment_score(self.text)
        return self._sentiment

    def __str__(self):
        return self.text


class Sentence(Text):
    ...


class Article(Text):
    def __init__(self, text, index=None):
        super(Article, self).__init__(text=text, index=index)
        self._sentence = None

    @property
    def sentence(self) -> Sentence:
        if self._sentence is None:
            _sentence = cut_sentence_loose(self.text)
            self._sentence = [Sentence(i) for i in _sentence]
        return self._sentence


if __name__ == '__main__':
    ...

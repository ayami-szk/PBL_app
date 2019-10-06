# -*- coding: utf-8 -*-
import json
import os
import re

import MeCab
import neologdn
import sengiri

re_delimiter = re.compile("[。,．!\?]")
NEGATION = ('ない', 'ず', 'ぬ')
DICT_DIR = os.path.join(os.path.dirname(__file__), 'dic')


class Analyzer(object):

    def __init__(self, mecab_args=''):
        self.word_dict = json.load(open(os.path.join(DICT_DIR, 'pn_noun.json')))
        self.wago_dict = json.load(open(os.path.join(DICT_DIR, 'pn_wago.json')))
        self.tagger = MeCab.Tagger(mecab_args)
        self.tagger.parse('')  # for avoiding bug

    def _lookup_wago(self, lemma, lemmas):
        if lemma in self.wago_dict:
            return 1 if self.wago_dict[lemma].startswith('ポジ') else -1
        for i in range(10, 0, -1):
            wago = ' '.join(lemmas[-i:]) + ' ' + lemma
            if wago in self.wago_dict:
                return 1 if self.wago_dict[wago].startswith('ポジ') else -1
        return None

    def _has_arujanai(self, substring):
        return 'あるじゃない' in substring

    def _calc_sentiment_polarity(self, sentence):
        polarities = []
        lemmas = []
        node = self.tagger.parseToNode(sentence)
        while node:
            if 'BOS/EOS' not in node.feature:
                surface = node.surface
                feature = node.feature.split(',')
                lemma = feature[6] if feature[6] != '*' else node.surface
                if lemma in self.word_dict:
                    polarity = 1 if self.word_dict[lemma] == 'p' else -1
                    polarities.append(polarity)
                else:
                    polarity = self._lookup_wago(lemma, lemmas)
                    if polarity is not None:
                        polarities.append(polarity)
                    elif polarities and surface in NEGATION:
                        polarities[-1] *= -1
                lemmas.append(lemma)
            node = node.next
        return polarities

    def count_polarity(self, text):
        """Calculate sentiment polarity counts per sentence
        Arg:
            text (str)
        Return:
            counts (list) : positive and negative counts per sentence
        """
        text = neologdn.normalize(text)
        counts = []
        for sentence in sengiri.tokenize(text):
            count = {'positive': 0, 'negative': 0}
            polarities = self._calc_sentiment_polarity(sentence)
            for polarity in polarities:
                if polarity == 1:
                    count['positive'] += 1
                elif polarity == -1:
                    count['negative'] += 1
                else:
                    pass
            counts.append(count)
        return counts
    
    def analyze(self, text):
        """Calculate sentiment polarity scores per sentence
        Arg:
            text (str)
        Return:
            scores (list) : scores per sentence
        """
        text = neologdn.normalize(text)
        scores = []
        for sentence in sengiri.tokenize(text):
            polarities = self._calc_sentiment_polarity(sentence)
            if polarities:
                scores.append(sum(polarities) / len(polarities))
            else:
                scores.append(0)
        return scores

# !/usr/bin/python
# -*- coding:utf-8 -*-

import numpy as np
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl


if __name__ == '__main__':
    f = open('..\\novel.txt', mode='r', encoding='utf-8')
    text = f.read()
    f.close()

    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=5)
    print('关键词：')
    for item in tr4w.get_keywords(10, word_min_len=1):
        print(item['word'], item['weight'])

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'no_stop_words')
    data = pd.DataFrame(data=tr4s.key_sentences)
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure(facecolor='w')
    plt.plot(data['weight'], 'ro-', lw=2, ms=5, alpha=0.7)
    plt.grid(b=True, ls=':', color='#606060')
    plt.xlabel('句子', fontsize=12)
    plt.ylabel('重要度', fontsize=12)
    plt.title('句子的重要度曲线', fontsize=15)
    plt.show()

    key_sentences = tr4s.get_key_sentences(num=20, sentence_min_len=4)
    for sentence in key_sentences:
        print(sentence['weight'], sentence['sentence'])

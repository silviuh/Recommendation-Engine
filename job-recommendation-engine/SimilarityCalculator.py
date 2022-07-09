import googletrans
import pandas as pd
import nltk
from googletrans import Translator
from nltk.corpus import stopwords
import re
import unidecode
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
from string import punctuation


class SimilarityCalculator:
    def __init__(self):
        return

    def truncate(self, num):
        return re.sub(r'^(\d+\.\d{,3})\d*$', r'\1', str(num))

    def common_words(self, l_1, l_2):
        matching_words = set.intersection(set(l_1), set(l_2))
        return matching_words

    def jaccard_similarity(self, list1, list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection
        return float(intersection) / union

    def compute_cosine_similarity(self, list1, list2):
        text_list = [' '.join(list2), ' '.join(list1)]
        cv = TfidfVectorizer()
        count_matrix = cv.fit_transform(text_list)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage = round(match_percentage, 2)

        return str(match_percentage)

    def get_frequency_table(self, list_1, list_2):
        freq_table = {}
        for word in list_1:
            if not word in list_2:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

        freq_table = dict(sorted(freq_table.items(), key=lambda item: item[1], reverse=True))

        pd.set_option('display.max_rows', 300)
        df = pd.DataFrame.from_dict(freq_table.items())

        df.columns = ['word', 'count']

        return df

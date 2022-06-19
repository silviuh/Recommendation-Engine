import json

import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class WordCrunchingEngine:
    def __init__(self):
        self.wn = nltk.WordNetLemmatizer()
        self.which_stopwords = None
        self.english_stopwords = nltk.corpus.stopwords.words('english')
        self.romanian_stopwords = nltk.corpus.stopwords.words('romanian')

    def truncate(self, num):
        return re.sub(r'^(\d+\.\d{,3})\d*$', r'\1', str(num))

    def concat(self, s):
        '''Concatenate words like "D A T A  S C I E N C E" to get "DATA SCIENCE"'''
        # add spaces at both end for better processing
        s = ' ' + s + ' '
        while True:
            # search if more than two alphabets are separated by space
            x = re.search(r"(\s[a-zA-Z]){2,}\s", s)
            if x is None:
                break
            # replace to get the concatenation
            s = s.replace(x.group(), ' ' + x.group().replace(' ', '') + ' ')
        return s

    def preprocess_text(self, document, stopwords):
        # convert to lower case
        document = str(document).lower()
        # replace unusual quotes with '
        document = document.replace("′", "'").replace("’", "'")
        # replace new line with space
        document = document.replace("\n", " ")
        # concatenate
        document = self.concat(document)
        # remove links
        document = re.sub(r"http\S+", "", document)

        # convert education degrees like B.Tech or BTech to a specified form
        document = re.sub(r"\s+b[.]?[ ]?tech[(. /]{1}", " btech bachelor of technology ", document)
        document = re.sub(r"\s+m[.]?[ ]?tech[(. ]{1}", " mtech master of technology ", document)
        document = re.sub(r"\s+b[.]?[ ]?a[(. ]{1}", " ba bachelor of arts ", document)
        document = re.sub(r"\s+m[.]?[ ]?a[(. ]{1}", " ma master of arts ", document)
        document = re.sub(r"\s+b[.]?[ ]?sc[(. ]{1}", " bsc bachelor of science ", document)
        document = re.sub(r"\s+m[.]?[ ]?sc[(. ]{1}", " msc master of science ", document)
        document = re.sub(r"\s+b[.]?[ ]?e[(. ]{1}", " beng bachelor of engineering ", document)
        document = re.sub(r"\s+m[.]?[ ]?e[(. ]{1}", " meng master of engineering ", document)
        document = re.sub(r"\s+b[.]?[ ]?c[.]?[ ]?a[(. ]{1}", " bca bachelor of computer applications ", document)
        document = re.sub(r"\s+m[.]?[ ]?c[.]?[ ]?a[(. ]{1}", " mca master of computer applications ", document)
        document = re.sub(r"\s+b[.]?[ ]?b[.]?[ ]?a[(. ]{1}", " bba bachelor of business administration ", document)
        document = re.sub(r"\s+m[.]?[ ]?b[.]?[ ]?a[(. ]{1}", " mba master of business administration ", document)

        # convert skills with special symbols to words
        document = document.replace("c++", "cplusplus")
        document = document.replace("c#", "csharp")
        document = document.replace(".net", "dotnet")

        # replace non alpha numeric character with space
        document = re.sub('\W', ' ', document)

        # if remove stop words flag set then remove them
        z = []
        for i in document.split():
            if i not in stopwords:
                # use lemmatizer to reduce the inflections
                i = self.wn.lemmatize(i)
                z.append(i)
        z = ' '.join(z)

        # strip white spaces
        z = z.strip()
        return list(z.split(" "))

    def clean_the_text(self, text, stopwords):
        # Replace non-word characters with empty space
        # text = re.sub('[^A-Za-z0-9\s]', ' ', text)

        # Remove punctuation
        text = ''.join([word for word in text if word not in string.punctuation])

        # Bring text to lower case
        text = text.lower()

        # Tokenize the text
        tokens = re.split('\W+', text)

        # Remove stopwords
        text = [word for word in tokens if word not in stopwords]

        # Lemmatize the words
        text = [self.wn.lemmatize(word) for word in text]

        # Return text
        return text

    def common_words(self, l_1, l_2):
        """
        Input:
            l_1: list of words
            l_2: list_of words
        Output:
            matching_words: set of common words exist in l_1 and l_2
        """
        matching_words = set.intersection(set(l_1), set(l_2))
        return matching_words

    def jaccard_similarity(self, list1, list2):
        intersection = len(list(set(list1).intersection(list2)))
        union = (len(set(list1)) + len(set(list2))) - intersection
        return float(intersection) / union

    def compute_cosine_similarity(self, list1, list2):
        # text_list = [cvContent, jobContent]
        text_list = [' '.join(list2), ' '.join(list1)]

        # print(text_list)

        # cv = CountVectorizer()
        cv = TfidfVectorizer()  # tfid is better because it penalizes the most recurring words regarded as stopwords
        # in my document
        count_matrix = cv.fit_transform(text_list)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage = round(match_percentage, 2)

        return str(match_percentage)

    def get_frequency_table(self, list_1, list_2):
        freq_table = {}

        # Create frequency table for the words that are not in the list_2 but in the list_1
        for word in list_1:
            if not word in list_2:
                if word in freq_table:
                    freq_table[word] += 1
                else:
                    freq_table[word] = 1

        # Sort the dictionary by values in descending order
        freq_table = dict(sorted(freq_table.items(), key=lambda item: item[1], reverse=True))

        # Create a pandas dataframe from the dictionary
        pd.set_option('display.max_rows', 300)
        df = pd.DataFrame.from_dict(freq_table.items())

        # Rename columns
        df.columns = ['word', 'count']

        # print('You can choose some words in the job posting from the table below to add your resume.')
        return df

    def matching_keywords(self, job_posting, resume, language):
        if language == "romanian":
            self.which_stopwords = self.romanian_stopwords
        elif language == "english":
            self.which_stopwords = self.english_stopwords

        # with open(job_posting, 'r') as f:
        #     job_posting = f.read()
        #
        # with open(resume, 'r') as f:
        #     resume = f.read()

        list_1 = self.preprocess_text(job_posting, self.which_stopwords)
        list_2 = self.preprocess_text(resume, self.which_stopwords)

        # print(list_1)
        # print(list_2)

        # Apply common_words function to the lists
        common_keywords = self.common_words(list_1, list_2)

        result = {
            "common_words": len(common_keywords),
            "words_percentage": self.truncate(len(common_keywords) / len(list_2) * 100),
            "cosine_similarity": self.truncate(self.compute_cosine_similarity(list_1, list_2)),
            "jaccard_similarity": self.truncate(self.jaccard_similarity(list_1, list_2) * 100)
            # "frequency_table": self.get_frequency_table(list_1, list_2)
        }

        return json.dumps(result)
        # Dictionary to JSON Object using dumps() method
        # Return JSON Object

        # Print number of matching words
        # print('The number of common words in your resume and the job posting is: {}'.format(len(common_keywords)), '\n')
        # # Print the percentage of matching words
        # print(
        #     '{:.0%} of the words in your resume are in the job description'.format(len(common_keywords) / len(list_2)),
        #     '\n')
        # print('{0} % is the value of the [COSINE] percentage computation on your set of lists'.format(
        #     self.compute_cosine_similarity(list_1, list_2)),
        #     '\n')
        # print('{:.0} is the value for the [JACCARD] Index Computation on your set of lists '.format(
        #     self.jaccard_similarity(list_1, list_2)),
        #     '\n')
        # print('the frequency table is: ')
        # print(self.get_frequency_table(list_1, list_2))
        # Create an empty dictionary


if __name__ == '__main__':
    engine = WordCrunchingEngine()
    # print(engine.matching_keywords('data/job_posting4.txt', 'data/Resume1.txt'))

import json

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


class WordCrunchingEngine:
    def __init__(self):
        self.wn = nltk.WordNetLemmatizer()
        self.english_stopwords = nltk.corpus.stopwords.words('english')
        self.romanian_stopwords = nltk.corpus.stopwords.words('romanian')
        self.translator = Translator()
        self.which_stopwords = self.english_stopwords

    def truncate(self, num):
        return re.sub(r'^(\d+\.\d{,3})\d*$', r'\1', str(num))

    def concat(self, s):
        s = ' ' + s + ' '
        while True:
            x = re.search(r"(\s[a-zA-Z]){2,}\s", s)
            if x is None:
                break
            s = s.replace(x.group(), ' ' + x.group().replace(' ', '') + ' ')
        return s

    def preprocess_text(self, document, stopwords):
        document = str(document).lower()
        document = document.replace("′", "'").replace("’", "'")
        document = document.replace("\n", " ")
        document = self.concat(document)
        document = re.sub(r"http\S+", "", document)
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
        document = document.replace("c++", "cplusplus")
        document = document.replace("c#", "csharp")
        document = document.replace(".net", "dotnet")
        document = re.sub('\W', ' ', document)

        z = []
        for i in document.split():
            if i not in stopwords:
                i = self.wn.lemmatize(i)
                z.append(i)
        z = ' '.join(z)

        z = z.strip()

        return list(z.split(" "))

    def clean_the_text(self, text, stopwords):
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        tokens = re.split('\W+', text)
        text = [word for word in tokens if word not in stopwords]
        text = [self.wn.lemmatize(word) for word in text]

        return text

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

    def string_to_list(self, string):
        r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
        list_res = (r.split(string))
        return list_res

    def matching_keywords(self, job, resume):
        # def matching_keywords(self, job, resume, ro_resume, en_resume, resume_detected_language):

        # try:
        #     if not (job == "" or job is None or resume == "" or resume is None):
        #         job_detected_langauge = self.translator.detect(str(job[:200]))
        #         if job_detected_langauge.lang == "ro":
        #             self.which_stopwords = self.romanian_stopwords
        #             resume = ro_resume
        #         elif job_detected_langauge.lang == "en":
        #             self.which_stopwords = self.english_stopwords
        #             resume = en_resume
        # except Exception as e:
        #     self.which_stopwords = self.english_stopwords

        common_keywords_in_job_title = 0
        total_words_in_the_job_title = 0
        common_keywords_in_job_title_percentage = 0

        have_the_same_location_score = 0
        job_location = unidecode.unidecode(job['jobLocation'])  # TODO OPTIMIZE
        job_name = self.string_to_list(unidecode.unidecode(job['jobName']).lower())
        job_location_copy = job_location
        job_posting = job['jobDescription']
        job_resume_without_accent = unidecode.unidecode(resume).lower()  # TODO OPTIMIZE

        if job_resume_without_accent is not None:
            job_location_copy = self.string_to_list(job_location.lower())  # TODO OPTIMIZE
            for word in job_location_copy:
                if word in job_resume_without_accent:  # TODO OPTIMIZE
                    have_the_same_location_score = 100
                    break
            for word in job_name:
                total_words_in_the_job_title += 1
                if word in job_resume_without_accent:
                    common_keywords_in_job_title += 1

        # print(str(have_the_same_location) + ' ' + job_location)
        # try:
        #     if not (job_posting == "" or job_posting is None or
        #             resume == "" or resume is None):
        #         resume_detected_language = self.translator.detect(str(resume))
        #         job_description_detected_language = self.translator.detect(str(job_posting))
        #
        #         if resume_detected_language.lang != job_description_detected_language.lang:
        #             if resume_detected_language.lang == "ro":
        #                 resume = self.translator.translate(resume, dest='en').text
        #             elif job_description_detected_language.lang == "ro":
        #                 job_posting = self.translator.translate(job_posting, dest='en').text
        #
        #         if resume_detected_language.lang == "ro":
        #             self.which_stopwords = self.romanian_stopwords
        #         elif resume_detected_language.lang == "en":
        #             self.which_stopwords = self.english_stopwords
        # except Exception as e:
        #     print('Failed to: ' + str(e))

        # with open(job_posting, 'r') as f:
        #     job_posting = f.read()
        #
        # with open(resume, 'r') as f:
        #     resume = f.read()

        list_1 = self.preprocess_text(job_posting, self.which_stopwords)
        list_2 = self.preprocess_text(resume, self.which_stopwords)

        common_keywords_in_job_title_percentage = (common_keywords_in_job_title / total_words_in_the_job_title) * 100
        common_keywords = self.common_words(list_1, list_2)
        common_words = len(common_keywords)
        words_percentage = self.truncate(len(common_keywords) / len(list_2) * 100)
        cosine_similarity_value = self.truncate(self.compute_cosine_similarity(list_1, list_2))
        jaccard_similarity = self.truncate(self.jaccard_similarity(list_1, list_2) * 100)

        cosine_similarity_multiply_coefficient = 0.0
        have_the_same_location_multiply_coefficient = 0.0
        common_keywords_in_job_title_coefficient = 0.15

        if float(
                cosine_similarity_value) <= 5:
            have_the_same_location_multiply_coefficient = 0.02
        else:
            have_the_same_location_multiply_coefficient = 0.10

        cosine_similarity_multiply_coefficient = 0.55 - have_the_same_location_multiply_coefficient
        jaccard_similarity_multiply_coefficient = 0.20
        words_percentage_multiply_coefficient = 1.00 \
                                                - cosine_similarity_multiply_coefficient \
                                                - jaccard_similarity_multiply_coefficient \
                                                - have_the_same_location_multiply_coefficient - common_keywords_in_job_title_coefficient

        score = self.truncate(
            float(cosine_similarity_multiply_coefficient) * float(cosine_similarity_value) \
            + float(jaccard_similarity_multiply_coefficient) * float(jaccard_similarity) \
            + float(words_percentage_multiply_coefficient) * float(words_percentage) \
            + float(have_the_same_location_multiply_coefficient) * float(have_the_same_location_score)
            + float(common_keywords_in_job_title_coefficient) * float(common_keywords_in_job_title_percentage)
        )

        # score = self.truncate(
        #     float(0.60) * float(cosine_similarity_value) +
        #     float(0.30) * float(jaccard_similarity) +
        #     float(0.10) * float(have_the_same_location_score)
        # )

        # score = self.truncate(
        #     float(1.00) * float(cosine_similarity_value))

        # #
        # result = {
        #     "job_ID": job_id,
        #     "job_Location": job_location,
        #     "job_name": job_name,
        #     "common_words": common_words,
        #     "words_percentage": words_percentage,
        #     "cosine_similarity": cosine_similarity_value,
        #     "jaccard_similarity": jaccard_similarity,
        #     "score": score
        #     # "frequency_table": self.get_frequency_table(list_1, list_2)
        # }

        result_data = {
            "common_words": common_words,
            "words_percentage": words_percentage,
            "cosine_similarity": cosine_similarity_value,
            "jaccard_similarity": jaccard_similarity,
            "score": score
        }

        job_enhanced_data = {
            '_id': str(job['_id']),
            'jobLocation': job['jobLocation'],
            'jobName': job['jobName'],
            'jobEmployer': job['jobEmployer'],
            'jobDate': job['jobDate'],
            'jobUrl': job['jobUrl'],
            'jobDescription': job['jobDescription'],
            'jobImageURL': job['jobImageURL'],
            'score': score,
            'title_common_nr_words': common_keywords_in_job_title,
            'title_common_percentage': common_keywords_in_job_title_percentage,
        }

        # TODO verifica aici daca trebuie sa faci json.dumps() de job si de result_data
        # result = {
        #     "job": job,
        #     "result_data": result_data
        # }
        # # return result

        return job_enhanced_data


def string_to_list(string):
    r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
    list_res = (r.split(string))
    return list_res


if __name__ == '__main__':
    print("hello")

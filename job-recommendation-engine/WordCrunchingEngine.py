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

    def string_to_list(self, string):
        r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
        list_res = (r.split(string))
        return list_res

    def matching_keywords(self, job, resume):
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


def string_to_list(string):
    r = re.compile(r'[\s{}]+'.format(re.escape(punctuation)))
    list_res = (r.split(string))
    return list_res


if __name__ == '__main__':
    print("hello")
    # have_the_same_location = 0
    #
    # job_location = "București, Baia Mare, Constanta  și alte 2 orașe"
    # resume = "iaca naa brasov timisoara BUCURESTI constantaa"
    # if resume is not None:
    #     job_location = string_to_list(job_location.lower())
    #     print(job_location)
    #     print(resume.lower())
    #     for word in job_location:
    #         if word in resume.lower():
    #             have_the_same_location = 100
    #             print("YES")
    #             break

    # import pprint
    #
    # # Array of JSON Objects
    # products = [{"banan": {"name": "HDD", "brand": "Samsung", "price": "$100"},
    #              "sanana": {"casa": "mare", "bani": "multi", "masina": "smechera"}
    #              },
    #             {"banan": {"name": "Monitor", "brand": "Dell", "price": "$120"},
    #              "sanana": {"casa": "mare", "bani": "multi", "masina": "smechera"}
    #              },
    #             {"banan": {"name": "Mouse", "brand": "Logitech", "price": "$10"},
    #              "sanana": {"casa": "mare", "bani": "multi", "masina": "smechera"}
    #              }]
    # '''
    # Print the sorted JSON objects in descending order
    # based on the price key value
    # '''
    # print("\nArray of JSON objects after sorting:")
    # products = sorted(products, key=lambda k: k['banan']['price'], reverse=True)
    # pprint.pprint((json.dumps(products)))

    # engine = WordCrunchingEngine()
    # translator = Translator()
    # f = open(
    #     '/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/data/Resume_romana.txt',
    #     'r')
    # if f.mode == 'r':
    #     if f.mode == 'r':
    #         contents = f.read()
    #         print("LIMBA ESTE: " + translator.detect(contents).lang)
    #         result = translator.translate(contents)
    #         print(result.text)

    #
    # print(engine.matching_keywords(
    #     "                   "
    #     ""
    #     ""
    #     ""
    #     "                                                                                                We are looking for an Internship to join our development team in Timisoara and follow the career path as a "
    #     "Software Integrator.",
    #     "Obiectiv profesional	Sa lucrez ca programator Web intr-o companie aflata in dezvoltare si sa contribui la "
    #     "cresterea renumelui si cotei de piata a acesteia.",
    #     "romanian", "32432434", "lucrator la PLUG"))

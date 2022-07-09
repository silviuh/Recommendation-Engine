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
import simplemma
from ResumeParser import ResumeParser


class TextPreprocessor:

    def __init__(self):
        self.wn = nltk.WordNetLemmatizer()
        self.english_stopwords = nltk.corpus.stopwords.words('english')
        self.romanian_stopwords = nltk.corpus.stopwords.words('romanian')
        self.translator = Translator()
        self.which_stopwords = self.english_stopwords

    def concat(self, s):
        s = ' ' + s + ' '
        while True:
            x = re.search(r"(\s[a-zA-Z]){2,}\s", s)
            if x is None:
                break
            s = s.replace(x.group(), ' ' + x.group().replace(' ', '') + ' ')
        return s

    def preprocess_text(self, document, stopwords, lemmatization_lang):
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

        # remove mentions
        document = re.sub("@\S+", " ", document)

        # remove hashtags
        document = re.sub("#\S+", " ", document)

        # remove tiks
        document = re.sub("\'\w+", '', document)

        # remove numbers
        document = re.sub(r'\w*\d+\w*', '', document)

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
                if lemmatization_lang == "ro":
                    i = simplemma.lemmatize(i, lang='ro')
                else:
                    i = self.wn.lemmatize(i)

                z.append(i)
        z = ' '.join(z)

        # strip white spaces
        z = z.strip()
        return list(z.split(" "))

    def clean_the_text(self, text, stopwords):
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        tokens = re.split('\W+', text)
        text = [word for word in tokens if word not in stopwords]
        text = [self.wn.lemmatize(word) for word in text]

        return text

    def compute_cosine_similarity(self, list1, list2):
        text_list = [' '.join(list2), ' '.join(list1)]
        cv = TfidfVectorizer()
        count_matrix = cv.fit_transform(text_list)
        print(count_matrix)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100
        match_percentage = round(match_percentage, 2)

        return str(match_percentage)

    def translate(self, job, resume, english_resume):
        lemmatization_lang = "en"
        stopwords = self.english_stopwords

        # if resume_detected_language == "ro":
        #     ro_resume = resume
        #     en_resume = translator.translate(resume, dest='en').text
        #     en_resume = english_resume
        # elif resume_detected_language == "en":
        #     ro_resume = translator.translate(resume, dest='ro').text
        #     en_resume = resume

        try:
            if not (job == "" or job is None or resume == "" or resume is None):
                job_detected_langauge = self.translator.detect(str(job[300]))
                if job_detected_langauge.lang == "ro":
                    stopwords = self.romanian_stopwords
                    lemmatization_lang = "ro"
                elif job_detected_langauge.lang == "en":
                    stopwords = self.english_stopwords
                    lemmatization_lang = "en"
        except Exception as e:
            self.which_stopwords = self.english_stopwords
            stopwords = self.english_stopwords

        if lemmatization_lang == "ro":
            return {"resume": resume, "job": job, "stopwords": stopwords, "lemmatization_lang": lemmatization_lang}
        elif lemmatization_lang == "en":
            return {"resume": english_resume, "job": job, "stopwords": stopwords,
                    "lemmatization_lang": lemmatization_lang}


if __name__ == '__main__':
    english_stopwords = nltk.corpus.stopwords.words('english')
    romanian_stopwords = nltk.corpus.stopwords.words('romanian')
    translator = Translator()

    request_data_1 = {
        "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/jobs-descriptions-test/1_job-python.txt"
    }
    request_data_2 = {
        "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/python-dev-scientist.txt"
    }
    request_data_3 = {
        "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/Model-CV-completat-aptitudini-Asistenta-medicala-1.pdf"
    }
    request_data_4 = {
        "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/jobs-descriptions-test/2_job_asistent_medical.txt"
    }
    request_data_5 = {
        "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/jobs-descriptions-test/3_job_asistent_medical_eng.txt"
    }
    document_parser = ResumeParser()
    resume = document_parser.parse_request_data(request_data_3)
    job = document_parser.parse_request_data(request_data_4)

    text_preprocessor = TextPreprocessor()

    configuration = text_preprocessor.translate(job, resume)
    resume_processed = text_preprocessor.preprocess_text(configuration["resume"], configuration["stopwords"],
                                                         configuration["lemmatization_lang"])
    job_processed = text_preprocessor.preprocess_text(configuration["job"], configuration["stopwords"],
                                                      configuration["lemmatization_lang"])

    print(len(resume_processed))
    print(len(job_processed))
    print(resume_processed)
    print(job_processed)

    print(text_preprocessor.compute_cosine_similarity(resume_processed, job_processed))

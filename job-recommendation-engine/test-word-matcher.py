import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

wn = nltk.WordNetLemmatizer()  # Lemmatizer
stopwords = nltk.corpus.stopwords.words('english')


def concat(s):
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


def preprocess_text(document):
    document = str(document).lower()
    document = document.replace("′", "'").replace("’", "'")
    document = document.replace("\n", " ")
    document = concat(document)
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
            i = wn.lemmatize(i)
            z.append(i)
    z = ' '.join(z)

    # strip white spaces
    z = z.strip()
    return list(z.split(" "))


def clean_the_text(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word not in stopwords]
    text = [wn.lemmatize(word) for word in text]
    return text


def common_words(l_1, l_2):
    matching_words = set.intersection(set(l_1), set(l_2))
    return matching_words


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(set(list1)) + len(set(list2))) - intersection
    return float(intersection) / union


def compute_cosine_similarity(list1, list2):
    text_list = [' '.join(list2), ' '.join(list1)]
    cv = TfidfVectorizer()
    count_matrix = cv.fit_transform(text_list)
    match_percentage = cosine_similarity(count_matrix)[0][1] * 100
    match_percentage = round(match_percentage, 2)

    return str(match_percentage)


def get_frequency_table(list_1, list_2):
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


def matching_keywords(job_posting, resume):
    with open(job_posting, 'r') as f:
        job_posting = f.read()

    with open(resume, 'r') as f:
        resume = f.read()

    list_1 = preprocess_text(job_posting)
    list_2 = preprocess_text(resume)

    print(list_1)
    print(list_2)
    common_keywords = common_words(list_1, list_2)

    print('The number of common words in your resume and the job posting is: {}'.format(len(common_keywords)), '\n')
    print('{:.0%} of the words in your resume are in the job description'.format(len(common_keywords) / len(list_2)),
          '\n')
    print('{0} % is the value of the [COSINE] percentage computation on your set of lists'.format(
        compute_cosine_similarity(list_1, list_2)),
        '\n')
    print('{:.0} is the value for the [JACCARD] Index Computation on your set of lists '.format(
        jaccard_similarity(list_1, list_2)),
        '\n')
    print('the frequency table is: ')
    print(get_frequency_table(list_1, list_2))


if __name__ == '__main__':
    matching_keywords('data/job_posting4.txt', 'data/Resume1.txt')

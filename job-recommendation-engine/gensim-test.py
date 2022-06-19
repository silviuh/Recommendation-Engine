import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spacy.matcher import PhraseMatcher
from collections import Counter
import en_core_web_sm

if __name__ == '__main__':

    with open('data/Resume3.txt', "r") as job:
        job_posting = job.readlines()

    with open('data/job_posting1.txt', "r") as job:
        resume = job.readlines()

    jobContent = ''
    for t in job_posting:
        jobContent = jobContent + t.lower().replace("'", '')

    cvContent = ''
    for r in resume:
        cvContent = cvContent + r.lower().replace("'", '')

    # print(cvContent)

    text_list = [cvContent, jobContent]

    print(cvContent)
    print(jobContent)
    print(text_list)

    cv = CountVectorizer()
    count_matrix = cv.fit_transform(text_list)
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)

    # print("your reusume matches about " + str(matchPercentage) + "% of the job description")
    # summarize(jobContent, ratio=0.2)

    # spNLP = spacy.load('en_core_web_sm')
    spNLP = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(spNLP.vocab)
    terms = jobContent.split('\n')
    patterns = [spNLP.make_doc(t) for t in terms]
    matcher.add("Spec", patterns)

    doc = spNLP(cvContent)
    matchkeywords = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        if len(span.text) > 3:
            matchkeywords.append(span.text)

    a = Counter(matchkeywords)
    # print(a)

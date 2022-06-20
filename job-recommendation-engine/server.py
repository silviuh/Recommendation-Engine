import json

from flask import Flask, request
from textblob import TextBlob
from WordCrunchingEngine import WordCrunchingEngine

app = Flask(__name__)


# GET requests will be blocked
@app.route('/get-score', methods=['POST'])
def get_score():
    request_data = request.get_json()
    result = {
        "data": ""
    }
    result_data = []

    for jobDescription in request_data['jobPosting']:
        if jobDescription['jobDescription'] == '' or request_data['resume'] == '':
            print("CACAMACA")
            continue

        print(result_data.append(
            word_crunching_engine.matching_keywords(jobDescription['jobDescription'], request_data['resume'],
                                                    request_data['language'], jobDescription['_id'],
                                                    jobDescription['jobName'])))

    result['data'] = result_data
    result = json.dumps(result)

    return result


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    app.run(host="localhost", port=8000, debug=True)

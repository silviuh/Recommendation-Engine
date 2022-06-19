import json

from flask import Flask, request
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

    # TODO
    # vezi cum faci si cu limba sa o iei in considerare ca sa nu ai rezultate egale cu 0
    # daca am cv in engleza, descriere in romana poate fac o traducere la backend si vice-versa

    for jobDescription in request_data['jobPosting']:
        result_data.append(
            word_crunching_engine.matching_keywords(jobDescription['jobDescription'], request_data['resume'],
                                                    request_data['language'], jobDescription['_id'],
                                                    jobDescription['jobName']))

    print(result_data)
    result['data'] = result_data
    result = json.dumps(result)

    return result


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    app.run(host="localhost", port=8000, debug=True)

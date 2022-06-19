from flask import Flask, request
from WordCrunchingEngine import WordCrunchingEngine

app = Flask(__name__)


# GET requests will be blocked
@app.route('/get-score', methods=['POST'])
def get_score():
    request_data = request.get_json()

    # print(request_data)
    #
    # language = None
    # framework = None
    # python_version = None
    # example = None
    # boolean_test = None
    #
    # if request_data:
    #     if 'language' in request_data:
    #         language = request_data['language']
    #
    #     if 'framework' in request_data:
    #         framework = request_data['framework']
    #
    #     if 'version_info' in request_data:
    #         if 'python' in request_data['version_info']:
    #             python_version = request_data['version_info']['python']
    #
    #     if 'examples' in request_data:
    #         if (type(request_data['examples']) == list) and (len(request_data['examples']) > 0):
    #             example = request_data['examples'][0]
    #
    #     if 'boolean_test' in request_data:
    #         boolean_test = request_data['boolean_test']

    # return word_crunching_engine.matching_keywords('data/job_posting4.txt', 'data/Resume1.txt')
    return word_crunching_engine.matching_keywords(request_data['jobPosting'], request_data['resume'])


if __name__ == '__main__':
    word_crunching_engine = WordCrunchingEngine()
    app.run(host="localhost", port=8000, debug=True)

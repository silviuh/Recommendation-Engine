import textract
import io
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator
from pdfminer3.converter import TextConverter
import os.path
from os import path
import io


class ResumeParser:

    def __init__(self):
        return

    def parse_request_data(self, request_data):
        if path.exists(request_data["resumePath"]):
            ext = os.path.splitext(str(request_data["resumePath"]))[-1].lower()
            if ext == '.pdf':
                resume = self.parse_pdf(request_data["resumePath"])
            elif ext == '.txt':
                resume = self.parse_txt(request_data["resumePath"])
            elif ext == ".doc" or ext == ".docx":
                resume = self.parse_word(request_data["resumePath"])
            else:
                resume = "file does not exist"

        return resume

    def parse_pdf(self, file_path):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(file_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

        converter.close()
        fake_file_handle.close()

        return text

    def parse_word(self, file_path):
        txt = textract.process(file_path).decode('utf-8')
        # return txt \
        #     .replace('\n', ' ') \
        #     .replace('\t', ' ')
        return txt
        # .replace('\n', ' ') \
        # .replace('\t', ' ')

    def parse_txt(self, file_path):
        resume = ''
        with open(file_path, 'r') as f:
            resume = f.read()  # Read whole file in the file_content string

        return resume


if __name__ == '__main__':
    request_data = {
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/CV_ROTARU_GEORGE.docx"
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/DocumentatieLicenta_MunteanuLetitia-corectat.pdf"
        # "resumePath": "/Users/silviuh1/WORKSPACE/DEV/FACULTATE/licenta/Recommendation-Engine/job-recommendation-engine/resume-extensions-test/python-dev-scientist.txt"
    }
    resumeParser = ResumeParser()
    print(resumeParser.parse_request_data(request_data))

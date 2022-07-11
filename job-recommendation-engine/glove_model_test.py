import re

import nltk
import numpy as np
from scipy import spatial
import gensim.downloader as api
from gensim.models import Word2Vec

from TextPreprocessor import TextPreprocessor

model = api.load('glove-wiki-gigaword-50')
# choose from multiple models https://github.com/RaRe-Technologies/gensim-data

s0 = 'Mark zuckerberg owns the facebook company'
s1 = 'Facebook company ceo is mark zuckerberg'
s2 = 'Microsoft is owned by Bill gates kaka fukanaa'
s3 = 'How to salata miere learn japanese fukanaa slq prst'

python_job = '''
Job Overview
We are looking for a Data Scientist who will support our product, sales, leadership and marketing teams with insights gained from analyzing company data. The ideal candidate is adept at using large data sets to find opportunities for product and process optimization and using models to test the effectiveness of different courses of action. They must have strong experience using a variety of data mining/data analysis methods, using a variety of data tools, building and implementing models, using/creating algorithms and creating/running simulations. They must have a proven ability to drive business results with their data-based insights. They must be comfortable working with a wide range of stakeholders and functional teams. The right candidate will have a passion for discovering solutions hidden in large data sets and working with stakeholders to improve business outcomes.

Responsibilities for Data Scientist
Work with stakeholders throughout the organization to identify opportunities for leveraging company data to drive business solutions.
Mine and analyze data from company databases to drive optimization and improvement of product development, marketing techniques and business strategies.
Assess the effectiveness and accuracy of new data sources and data gathering techniques.
Develop custom data models and algorithms to apply to data sets.
Use predictive modeling to increase and optimize customer experiences, revenue generation, ad targeting and other business outcomes.
Develop company A/B testing framework and test model quality.
Coordinate with different functional teams to implement models and monitor outcomes.
Develop processes and tools to monitor and analyze model performance and data accuracy.
Qualifications for Data Scientist
Strong problem solving skills with an emphasis on product development.
Experience using statistical computer languages (R, Python, SLQ, etc.) to manipulate data and draw insights from large data sets.
Experience working with and creating data architectures.
Knowledge of a variety of machine learning techniques (clustering, decision tree learning, artificial neural networks, etc.) and their real-world advantages/drawbacks.
Knowledge of advanced statistical techniques and concepts (regression, properties of distributions, statistical tests and proper usage, etc.) and experience with applications.
Excellent written and verbal communication skills for coordinating across teams.
A drive to learn and master new technologies and techniques.
We’re looking for someone with 5-7 years of experience manipulating data sets and building statistical models, has a Master’s or PHD in Statistics, Mathematics, Computer Science or another quantitative field, and is familiar with the following software/tools:
Coding knowledge and experience with several languages: C, C++, Java,
JavaScript, etc.
Knowledge and experience in statistical and data mining techniques: GLM/Regression, Random Forest, Boosting, Trees, text mining, social network analysis, etc.
Experience querying databases and using statistical computer languages: R, Python, SLQ, etc.
Experience using web services: Redshift, S3, Spark, DigitalOcean, etc.
Experience creating and using advanced machine learning algorithms and statistics: regression, simulation, scenario analysis, modeling, clustering, decision trees, neural networks, etc.
Experience analyzing data from 3rd party providers: Google Analytics, Site Catalyst, Coremetrics, Adwords, Crimson Hexagon, Facebook Insights, etc.
Experience with distributed data/computing tools: Map/Reduce, Hadoop, Hive, Spark, Gurobi, MySQL, etc.
Experience visualizing/presenting data for stakeholders using: Periscope, Business Objects, D3, ggplot, etc.
'''

python_resume = '''
Charles K. Sorensen, MTA

Python Developer

3689 Parrish Avenue

Victoria, TX 77901

830-994-8344

 

Summary


 

Experience

 

Python Developer
March 2015-present

Handled programming tasks for and maintained 7 internal websites with a high success rate (97%) in product update deployment.
Developed a marketing lead MySQL database, collecting, categorizing, and filtering leads from various stakeholders, i.e., www, social media channels, or newsletters.
Led sprint planning meetings and divided tasks between a 15-person project team.
Tutored at three high schools every year, teaching young kids how to code in Python.
Key achievement: Designed a new feature for the company’s email marketing tool (MailSent) in 7 Active Days, contributing to the marketing department’s win in the IAC award competition in the Best Email Message Campaign category.

 

Data Scientist

PyMe, Victoria, TX

April 2012-February 2015

Automated and optimized collecting data using SQL, reaching over a 35% system’s response time boost.
Collaborated cross-departmentally on RPA to streamline issue management and migrate the current environments to the cloud, reducing the investment risk by 48%.
 

Education

 

2011 M.S. in Engineering

University of Texas, Austin, TX

 

Skills

 

Python, JavaScript, CSS3, HTML5, SQL
ORM libraries
Web frameworks: Django
MVC and MVT Architecture
Design skills
Problem-solving skills
Communication skills
Data visualization
Agile frameworks
 

Courses and Certificates

 

PCPP1 – Certified Professional in Python
MTA 98-381 – Microsoft Technical Associate
PSM II Assessment Certificate – Professional Scrum Master
 

Conferences

 

PyCon, every-year attendee since 2018
DjangoCon, 2020
'''

medical_assistant_job_desc = '''
Brief description of the company
800.000. This is the number of patients who have crossed our threshold during a year. 1200 is the number of professionals who are part of the Affidea Romania team and who, through concern, integrity and mutual respect, manage to reward the trust that patients and doctors put in our hands.

Requirements
-Generalist Postgraduate School of Health;
-Compliance with the code of professional ethics and the rules governing the profession of medical assistant in Romania;
-Good computer user

Responsibilities
-Greet clients arriving at the clinic and provide them with the requested information, perform triage, direct them to the medical office where the investigation will take place;
-Assisting the doctor in carrying out clinical investigations, performing functional explorations, filling in patient records and clinical medical observation documents, preventing the creation of infection outbreaks, sterilizing instruments and materials, ensuring the general hygienic and sanitary conditions in the workplace,
Other information
Affidea Romania, Affidea-SANMED, Affidea-Phoenix and Affidea-Hiperdia clinics are part of the Affidea Group, headquartered in Amsterdam, Europe's leading provider of diagnostic imaging, outpatient and cancer treatment services.
The Affidea Group provides leading medical services through its 246 high-performance diagnostic imaging clinics, medical laboratories and cancer treatment centres, using the latest and most modern technology worldwide.
The Affidea Group currently operates in 16 countries: Ireland, UK, Poland, Czech Republic, Switzerland, Hungary, Croatia, Bosnia and Herzegovina, Romania, Italy, Lithuania, Portugal, Greece, Serbia, Spain, Turkey.
Affidea Romania, Affidea-SANMED, Affidea-Phoenix and Affidea-Hiperdia offer a full range of professional radiology imaging, nuclear medicine, clinical consultations and laboratory services through 36 clinics in 19 counties, benefiting from the expertise of over 800 healthcare professionals.

Affidea figures in Romania
36 clinics
2 PET/CT machines and 1 SPECT/CT machine
24 CT scanners
26 MRI scanners
136 diagnostic imaging equipment
800 staff
800 000 patients/year
36 years of combined experience Affidea Romania + Hiperdia

Affidea Fundeni Centre received the EuroSafe "5 Stars" award from the European Society of Radiology, which is a recognition of the company's ability to provide excellence in radiation protection and patient safety.
Affidea Fundeni Clinic is accredited by the European Association of Nuclear Medicine (EANM), the highest recognition for excellence in nuclear medicine.
Affidea Fundeni is the largest high-performance diagnostic imaging and nuclear medicine centre in Romania, offering an extensive range of medical services such as PET/CT, SPECT/CT, MRI, CT, 3D Mammography with Tomosynthesis, as well as other imaging investigations, laboratory analyses, clinical consultations, day hospitalisation in the specialties of oncology and neurology.


Translated with www.DeepL.com/Translator (free version)

'''

construction_job = '''
SCHUMACHER HOMES AWARDED TOP WORKPLACE 2021
 

4-DAY/36 HOUR FLEXIBLE WORK WEEK - Our employees drive our success and we show our appreciation by committing to offering a flexible work schedule to enhance work/life balance.

 

We are an award-winning company which strives to be the best on your lot custom homebuilder providing the ultimate customer experience.  We are the recipient of the National Housing Quality Award for excellence in construction standards and customer satisfaction and  the recipient of the NAHB’s National Gold Winning Home of the Year demonstrating our continued leadership in architecture and design.

 

Quite simply, no one builds a better home or offers a better place to work. Apply today to join our outstanding team..
 

Our Columbus, OH location at 5087 Columbus Pike, Lewis Center, OH 43035 is looking for a Residential Construction Manager to join its team.  Our Construction Managers/Job Superintendents must be proficient in understanding residential construction systems. This position offers a competitive salary, bonus incentive, company vehicle, plus advancement potential. Under the direction of the General Manager and/or the Production Manager, the Construction Manager/Superintendent is responsible for working with the customers to build their homes, schedule trades and ensure the homes are built with attention to quality, meeting building time expectations and exceeding homeowner satisfaction.

 

SPECIFIC RESPONSIBILITIES:

Builds assigned homes within time, cost, quality and satisfaction standards (within allowed performance tolerances).
Run home site inspection meeting with homeowner. Document lot conditions re: house location, etc. on plot plan.
Participate in pre-construction meeting with General Manager, Customer Coordinators and homeowners.
Approve all purchase orders for payment once work is completed and materials delivered 100%.
Attends other required meetings as requested.
Inspect each assigned job.
Recruit trade partners.
Conducts homeowner orientation meeting with customers.
Responsible for completion of 100% of homeowner punch list items within 14 days.
Maintains cleanliness or and maintenance schedule for assigned vehicle.
Initiates contact via phone, letter, e-mail or in person with each customer under construction.
Residential Construction Manager/Superintendent: Think about this -- After training is completed, we offer a

4-DAY/36 HOUR FLEXIBLE WORK WEEK, as well as a very competitive salary, and bonus incentive. We also offer a comprehensive medical, dental, vision, life insurance plans, PTO (Paid Time Off), a homebuilding discount, and paid holidays. Additionally, we partner with Fidelity to offer a premier 401k Plan + employer match. If you’re interested in being part of our dynamic growth, plus an integral part of a company who believes in working hard, having fun and producing results APPLY TODAY!

WORK HARD, HAVE FUN, PRODUCE RESULTS
Requirements
Prior scattered-site residential construction experience (preferred).
Technical residential construction knowledge to understand construction processes and terminology to assist in management of field personnel and systems.
Effective time management skills to manage a busy work environment. The ability to schedule and organize multiple jobs is critical.
Computer experience – the ability to use technology (Smart Phone, I-Pad). Experience with Microsoft Outlook for email correspondence.
Keywords: construction manager, project manager, construction superintendent, superintendent, homebuilder, custom homebuilder, residential construction, scattered-site residential

Categories
'''


def truncate(num):
    return re.sub(r'^(\d+\.\d{,3})\d*$', r'\1', str(num))


def preprocess(s):
    return [i.lower() for i in s.split()]


def get_vector(s):
    array_of_models = []
    for i in text_preprocessor.preprocess_text(s, english_stopwords, 'en'):
        try:
            array_of_models.append(model[i])
        except Exception as e:
            do_nothing = ''

    return np.sum(np.array(array_of_models), axis=0)
    # return np.sum(np.array([model[i] for i in text_preprocessor.preprocess_text(s, english_stopwords, 'en')]), axis=0)


if __name__ == '__main__':
    text_preprocessor = TextPreprocessor()
    english_stopwords = nltk.corpus.stopwords.words('english')

    # sentences = []
    # sentences.append(text_preprocessor.preprocess_text(python_job, english_stopwords, 'en'))
    # sentences.append(text_preprocessor.preprocess_text(python_resume, english_stopwords, 'en'))
    # sentences.append(text_preprocessor.preprocess_text(medical_assistant_job_desc, english_stopwords, 'en'))
    # sentences.append(text_preprocessor.preprocess_text(construction_job, english_stopwords, 'en'))
    # model = Word2Vec(sentences, min_count=1)
    #
    # print(model)
    # model.save('model.bin')
    # new_model = Word2Vec.load('model.bin')
    # print(new_model)

    # print('s0 vs s1 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s1)))
    # print('s0 vs s2 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s2)))
    # print('s0 vs s3 ->', 1 - spatial.distance.cosine(get_vector(s0), get_vector(s3)))
    print('python job vs python resume ->',
          1 - spatial.distance.cosine(get_vector(construction_job), get_vector(python_resume)))

    # print(get_vector(s2))

    # for word in preprocess(s3):
    #     try:
    #         # print(model.most_similar(word))
    #         print(model(word))
    #     except Exception as e:
    #         print(e)

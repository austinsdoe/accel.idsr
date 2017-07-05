from flask import request, url_for
from urlparse import urlparse, urljoin

# http://flask.pocoo.org/snippets/62/
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.values.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def redirect_back(endpoint, **values):
    target = request.form['next']
    if not target or not is_safe_url(target):
        target = url_for(endpoint, **values)
    return redirect(target)

# Headers to appear while exporting IDSR Forms as a CSV. Keys are texts how they are going to appear in file header,
# values are field name from MongoDB.
CSV_HEADERS = [{"CREATED BY": "createdby"},
               {"BIKA STATUS": "bika-status"},
               {"IS PARTIAL": "is_partial"},
               {"COUNTY": "county_code_text"},
               {"DISTINCT": "reporting_distinct_text"},
               {"CLIENT": "reporting_health_facility_text"},
               {"CLIENT PATIENT ID": "patient_client_patientid"},
               {"CASE ID": "case_id"},
               {"DIAGNOSIS": "diagnosis_text"},
               {"PATIENT FIRST NAME": "patient_firstname"},
               {"PATIENT LAST NAME": "patient_lastname"},
               {"PATIENT DATE OF BIRTH": "patient_dateofbirth"},
               {"PATIENT GENDER": "patient_gender_text"},
               {"PATIENT COUNTY OF RESIDENCE": "patient_county_of_residence_text"},
               {"PATIENT DISTRICT OF RESIDENCE": "patient_district_of_residence_text"},
               {"PATIENT COMMUNITY OF RESIDENCE": "patient_community_of_residence"},
               {"DATE OF ONSET": "case_date_of_onset"},
               {"DATE SEEN": "case_date_seen"},
               {"REPORTING PERSON FIRSTNAME": "reporting_person_firstname"},
               {"REPORTING PERSON LASTNAME": "reporting_person_lastname"},
               {"REPORTING PERSON PHONE": "reporting_person_phone"},
               {"SAMPLER NAME": "sampler_name"},
               {"SAMPLER PHONE": "sampler_phone"},
               {"COMMENTS": "health_worker_comments"},
               {"VACCINATED?": "vaccinated_for_disease"},
               {"# OF VACCINATION": "number_of_vaccinations"},
               {"MOST RECENT VACCINATION DATE": "date_of_most_recent_vaccination"},
               {"DATE OF SPECIMEN COLLECTION": "date_sampled"},
               {"DATE OF SPECIMEN SENT TO LAB": "date_specimen_sent"},
               {"SAMPLE TYPE": "sample_type_text"},
               {"LAB ANALYSIS REQUESTED": "analyses_requested_text"}]

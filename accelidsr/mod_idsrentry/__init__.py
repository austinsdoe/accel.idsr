from accelidsr import db
import pymongo

counties_districts = {
    "Bomi": ["Dewoin", "Klay", "Mecca", "Senjeh"],
    "Bong": ["Fuamah", "Jorquelleh", "Kokoyah", "Panta-Kpa", "Salala", "Sanayea ", "Suakoko", "Zota"],
    "Gbarpolu": ["Belleh", "Bopolu", "Bokomu", "Kongba", "Gbarma"],
    "Grand Bassa": ["District #1", "District #2", "District #3", "District #4", "Owensgrove", "St. John River"],
    "Grand Cape Mount": ["Commonwealth", "Garwula", "Gola Konneh", "Porkpa", "Tewor"],
    "Grand Gedeh": ["Gbarzon", "Konobo", "Tchien"],
    "Grand Kru": ["Buah", "Lower Kru Coast", "Sasstown", "Upper Kru Coast"],
    "Lofa": ["Foya", "Kolahun", "Salayea", "Vahun", "Voinjama", "Zorzor"],
    "Margibi": ["Firestone", "Gibi", "Kakata", "Mambah-Kaba"],
    "Maryland": ["Barrobo", "Pleebo/Sodeken"],
    "Montserrado": ["Careysburg", "Greater Monrovia", "Commonwealth", "St. Paul River", "Todee"],
    "Nimba": ["Gbehlageh", "Saclepea", "Sanniquelleh-Mahn", "Tappita", "Yarwein-Mehnsohnneh", "Zoegeh"],
    "River Gee": ["Gbeapo", "Webbo"],
    "Rivercess": ["Morweh", "Timbo"],
    "Sinoe": ["Butaw", "Dugbe River", "Greenville", "Jaedae Jaedepo", "Juarzon", "Kpayan", "Pyneston"]
}
diseases = [
    ('cholera', 'Cholera'),
    ('human_rabies', 'Human Rabies'),
    ('lassa_fever', 'Lassa fever'),
    ('measles', 'Measles'),
    ('meningitis', 'Meningitis'),
    ('vhf', 'VHF (EVD)'),
    ('yellow_fever', 'Yellow Fever'),
    ('maternal_death', 'Maternal Death'),
    ('nenoatal_death', 'Neonatal Death'),
    ('acute_bloody_diarrhea', 'Acute Bloody Diarrhea (Shigellosis)'),
    ('u_cluster_death', 'Member of Unexplained Cluster of Death'),
    ('u_cluster_disease', 'Member of Unexplained Cluster of Disease'),
    ('_other', 'Other')
]
case_outcomes = [
    ('alive', 'Alive'),
    ('dead', 'Dead (deceased)'),
]
case_classifications = [
    ('', 'Select...'),
    ('confirmed', 'Confirmed'),
    ('suspected', 'Suspected')
]
specimen_types = [
    ('', 'Select...'),
    ('semen_evd', 'Semen (EVD)'),
    ('serum_evd', 'Serum (EVD)'),
    ('swabs_evd', 'Swabs (EVD)'),
    ('whole_blood_evd', 'Whole Blood (EVD)'),
]
analysis_profiles = [
    ('', 'Select...'),
    ('genexpert_evd', 'GeneXpert EVD')
]


def getCountiesChoices():
    """
    Returns a list of 2-tuples that contains the counties available in the
    system, sorted by the county name asc. Each element within the list is a
    2-tuple, where the first element is the value to be used in the html
    control and the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']

    :return: A list of 2-tuples with the counties sorted by name ascending,
        with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    records = db['counties'].find().sort([
                    ("title", pymongo.ASCENDING)
                ])
    choices = [(r['code'], r['title']) for r in records]
    choices.insert(0, ('', 'Select...'))
    return choices


def getDistrictChoices(county=None):
    """
    Returns a list of 2-tuples that contains the districts available in the
    system for the county passed in, sorted by the district name asc. Each
    element within the list is a 2-tuple, where the first element is the value
    to be used in the html control and the second item is the text to be
    displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']
    If no county is passed in, a list with only the first record 'Select...'
    is returned.

    :param county: A single string that identifies a county code
    :type county: string
    :return: A list of 2-tuples with the districts sorted by name ascending,
        with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    choices = []
    if county:
        query = {'county_code': county}
        records = db['districts'].find(query).sort([
                        ("title", pymongo.ASCENDING)
                    ])
        choices = [(r['title'], r['title']) for r in records]
    choices.insert(0, ('', 'Select...'))
    return choices


def getFacilityChoices(county=None, district=None):
    """
    Returns a list of 2-tuples that contains the health facilities available in
    the system for the county and district passed in, sorted by the district
    name asc. Each element within the list is a 2-tuple, where the first
    element is the value to be used in the html control and the second item is
    the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']
    If no county and/or no district is passed in, a list with only the first
    record 'Select...' is returned.

    :param county: A single string that identifies a county
    :type county: string
    :param district: A single string that identifies a district
    :type district: A string
    :return: A list of 2-tuples with the facilities sorted by name ascending,
        with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    choices = []
    if county and district:
        records = db['counties'].find({'code': county}).sort([
                        ("title", pymongo.ASCENDING)
                    ])
        title = county
        if records:
            title = records[0]['title']
        query = {'county': title, 'district': district}
        records = db['facilities'].find(query).sort([
                        ("code", pymongo.ASCENDING)
                    ])
        choices = [(r['uid'], r['title']) for r in records]
    choices.insert(0, ('', 'Select...'))
    return choices


def getDiagnosisChoices():
    """
    Returns a list of 2-tuples that contains the diagnosis available in the
    system, sorted by name asc. Each element within the list is a 2-tuple,
    where the first element is the value to be used in the html control and
    the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the last position:
    [('_other'), 'Other']

    :return: A list of 2-tuples with the counties sorted by name ascending,
        with an additional item in last position ('_other', 'Other')
    :rtype: A list of 2-tuples
    """
    choices = []
    records = db['diseases'].find().sort([
                    ("title", pymongo.ASCENDING)
                ])
    choices = [(r['uid'], r['title']) for r in records]
    choices.append(('_other', 'Other'))
    return choices


def getCaseOutcomeChoices():
    """
    Returns a list of 2-tuples that contains the case outcomes available in the
    system, sorted by name asc. Each element within the list is a 2-tuple,
    where the first element is the value to be used in the html control and
    the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]

    :return: A list of 2-tuples with the counties sorted by name ascending
    :rtype: A list of 2-tuples
    """
    choices = []
    records = db['caseoutcomes'].find().sort([
                    ("title", pymongo.ASCENDING)
                ])
    choices = [(r['uid'], r['title']) for r in records]
    choices.append(('_other', 'Other'))
    return choices


def getCaseClassificationChoices():
    """
    Returns a list of 2-tuples that contains the clinical case classifications
    available in the system, sorted by name asc. Each element within the list
    is a 2-tuple, where the first element is the value to be used in the html
    control and the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']

    :return: A list of 2-tuples with the clinical case classifications sorted
        by name ascending, with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    # TODO Get available case classifications from Bika instance
    return case_classifications


def getSpecimenTypeChoices():
    """
    Returns a list of 2-tuples that contains the specimen types (sample types)
    available in the system, sorted by name asc. Each element within the list
    is a 2-tuple, where the first element is the value to be used in the html
    control and the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']

    :return: A list of 2-tuples with the specimen types (sample types) sorted
        by name ascending, with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    choices = []
    records = db['sampletypes'].find().sort([
                    ("title", pymongo.ASCENDING)
                ])
    choices = [(r['uid'], r['title']) for r in records]
    choices.insert(0, ('', 'Select...'))
    return choices

def getAnalysisProfileChoices():
    """
    Returns a list of 2-tuples that contains the analysis profiles (tests)
    available in the system, sorted by name asc. Each element within the list
    is a 2-tuple, where the first element is the value to be used in the html
    control and the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']

    :return: A list of 2-tuples with the specimen types (sample types) sorted
        by name ascending, with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    choices = []
    records = db['analysisprofiles'].find().sort([
                    ("title", pymongo.ASCENDING)
                ])
    choices = [(r['uid'], r['title']) for r in records]
    choices.insert(0, ('', 'Select...'))
    return choices

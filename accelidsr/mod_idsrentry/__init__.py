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

def getCountiesChoices():
    """
    Returns a list of 2-tuples that contains the countries available in the
    system, sorted by the country name asc. Each element within the list is a
    2-tuple, where the first element is the value to be used in the html
    control and the second item is the text to be displayed:
    [('val1', 'text1'), (val2, text2)]
    An additional tuple is added in the first position:
    [(''), 'Select...']

    :return: A list of 2-tuples with the counties sorted by name ascending, with
        an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    # TODO Get available counties from Bika instance
    counties = counties_districts.keys()
    counties.sort()
    choices = [(c, c) for c in counties]
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

    :param county: A single string that identifies a county
    :type county: string
    :return: A list of 2-tuples with the districts sorted by name ascending,
        with an additional item in position 0: ('', 'Select...')
    :rtype: A list of 2-tuples
    """
    districts = []
    if county:
        # TODO Get available districts from Bika instance
        districts = counties_districts.get(county, [])
    choices = [(d, d) for d in districts]
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
    facilities = []
    if county and district:
        # TODO Get available facilities from Bika instance
        facilities = [{'uid': 'fake-1', 'title': 'Facility fake 1'},
                      {'uid': 'fake-2', 'title': 'Facility fake 2'}]
    choices = [(f['uid'], f['title']) for f in facilities]
    choices.insert(0, ('', 'Select...'))
    return choices

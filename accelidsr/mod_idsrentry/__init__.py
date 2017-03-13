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
    counties = counties_districts.keys()
    counties.sort()
    choices = [(c, c) for c in counties]
    choices.insert(0, ('', 'Select...'))
    return choices

def getDistrictChoices(county):
    districts = []
    if county:
        districts = counties_districts.get(county, [])
    choices = [(d, d) for d in districts]
    choices.insert(0, ('', 'Select...'))
    return choices

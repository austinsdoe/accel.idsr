#!/usr/bin/env python

from flask import Flask
from flask import render_template
from jsonapi import JSONAPI

app = Flask(__name__)

jsonapi = JSONAPI()


@app.route('/')
def index():
    return render_template('index.html')


def get_facilities_data():
    """Query for all facilities, states and districts in the LIMS.
    """
    data = jsonapi.read(
        portal_type='Client',
        include_fields="ClientID,Title,State,District",
    )
    facilities = {}
    for item in data['objects']:
        code = item['ClientID']
        title = item['Title']
        state = item['State']
        district = item['District']
        if state not in facilities:
            facilities[state] = {}
        if district not in facilities[state]:
            facilities[state][district] = []
        facilities[state][district].append({'code': code, 'title': title})
    return facilities

@app.route('/idsr-input-minimal')
def idsr_input_minimal():
    """The main view for the idsr nested steps wizards page.
    """
    # Any variables that are needed in the templates can be included
    # in kwargs, and will be available in the templates by using the syntax
    # {{ variable_name }}
    districts, facilities = get_facilities_data()
    kwargs = {
        'facilities': facilities,
    }
    return render_template('idsr-input-minimal.html', **kwargs)

if __name__ == "__main__":
    app.run()

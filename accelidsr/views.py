from accelidsr import app
from flask import Flask
from flask import render_template
from flask import session, redirect, g, url_for, flash
from flask import request, redirect
from flask_login import current_user, login_user, logout_user, LoginManager, login_required
from jsonapi import JSONAPI
from arcreation import ARCREATION
import os
import flask_login
import bcrypt
import json


@app.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        # Load app's main page
        return render_template('dataclerk_task_selection.html', user=current_user)
    else:
        # Redirect to login page
        return redirect(url_for('login'))

@app.route('/dataclerk-task-selection')
@login_required
def dataclerk_task_selection():
    return render_template("dataclerk_task_selection.html")


@app.route('/idsr-partial')
@login_required
def idsr_partial():
    """
    Display the quick input IDSR form
    """

    return render_template('idsr-partial.html')


@app.route('/idsr-form')
@login_required
def idsr_form():
    """
    Display the quick input IDSR form
    """

    return render_template('full_idsr_form.html')


@app.route('/idsr-form-p', methods=['POST', 'GET'])
@login_required
def idsr_form_p():
    """The main view for the idsr nested steps wizards page.
    """
    idsr_data = dict()
    result = dict()

    if request.method == 'POST':
        result = request.form

    if result:
        idsr_data = result.to_dict()

        client_data = arcreation.create_client_full(**idsr_data)
        client_contact_data = arcreation.create_client_contact(client_data, **idsr_data)
        patient_data = arcreation.create_reg_patient_full(client_data, **idsr_data)
        ar_data = arcreation.create_analysis_request(client_data, client_contact_data, patient_data, **idsr_data)

        idsr_data['bika_client_id'] = client_data['obj_id']
        idsr_data['bika_patient_id'] = patient_data['obj_id']
        idsr_data['bika_ar_id'] = ar_data['ar_id']
        idsr_data['_id'] = patient_data['obj_id']
        idsr_data['totally_filled'] = 'True'

        db = mongo.get_db()
        mongo.add_idsr(idsr_data, db)

        return render_template("dataclerk_task_selection.html", result=idsr_data)

    return render_template('full_idsr_form.html')


@app.route('/full-idsr-filled-with-partial-info', methods=['POST', 'GET'])
@login_required
def idsr_complete_partial_input():
    """The main view for the idsr nested steps wizards page.
    """
    idsr_data = dict()
    result = dict()

    if request.method == 'POST':
        result = request.form

    if result:
        idsr_data = result.to_dict()

        idsr_data['totally_filled'] = 'True'

        db = mongo.get_db()
        mongo.add_idsr_partial_full(idsr_data, db)  # update the previous record

        bika_data = mongo.get_document_by_id(idsr_data, db)  # get entire record from DB

        partial = {}
        records = dict((record['_id'], record) for record in bika_data)

        for k, v in records.items():
           partial = v

        arcreation.update_client(**partial)
        arcreation.update_patient(**partial)


        return render_template("dataclerk_task_selection.html", result=partial)

    return render_template('dataclerk_task_selection.html')

@app.route('/store_quick_idsr', methods=['POST', 'GET'])
@login_required
def store_quick_idsr():

    """
    Get Quick IDSR input and create an AR.
    Store data in mongo db database
    if no data is in array, start over.
    """

    idsr_data = {}
    result = dict()

    if request.method == 'POST':
        result = request.form

    if result:

        idsr_data = result.to_dict()

        client_data = arcreation.create_client(**idsr_data)
        client_contact_data = arcreation.create_client_contact(client_data, **idsr_data)
        patient_data = arcreation.create_reg_patient(client_data, **idsr_data)
        ar_data = arcreation.create_analysis_request(client_data, client_contact_data, patient_data, **idsr_data)


        idsr_data['bika_client_id'] = client_data['obj_id']
        idsr_data['bika_patient_id'] = patient_data['obj_id']
        idsr_data['bika_ar_id'] = ar_data['ar_id']
        idsr_data['_id'] = patient_data['obj_id']
        idsr_data['patient_record_id_old'] = idsr_data['patient_record_id']
        idsr_data['patient_record_id']=patient_data['obj_id']
        idsr_data['totally_filled'] = 'False'

        db = mongo.get_db()
        mongo.add_idsr(idsr_data, db)

        return render_template("dataclerk_task_selection.html", result=idsr_data)
    else:
        return render_template("dataclerk_task_selection.html", result=idsr_data)


@app.route('/idsr-partial/<string:patient_id>')
@login_required
def idsr_complete(patient_id):
    """
    Receive the patient ID of a partially filled IDSR record
    Get the document associated with the ID
    Pass the data to the HTML pages to autofilled the previously filled fields
    """

    db = mongo.get_db()
    partially_filled = (mongo.get_partial_idsr(db))

    partial = {}
    records = dict((record['_id'], record) for record in partially_filled)

    for k, v in records.items():
        partial = v

    return render_template('full_idsr_filled_with_partial_info.html', result=partial)

@app.route('/incomplete-idsr')
@login_required
def incomplete_idsr( ):
    """
    Receive the patient ID of a partially filled IDSR record
    Get the document associated with the ID
    Pass the data to the HTML pages to autofilled the previously filled fields
    """

    db = mongo.get_db()
    partially_filled = (mongo.get_partial_idsr(db))

    partial = []
    for object in partially_filled:
        partial.append(object)


    return render_template('incomplete_idsr.html', result=partial)

@app.route('/idsr-reports')
@login_required
def idsr_reports( ):
    """
    Receive the patient ID of a partially filled IDSR record
    Get the document associated with the ID
    Pass the data to the HTML pages to autofilled the previously filled fields
    """

    db = mongo.get_db()
    partially_filled = (mongo.get_partial_idsr(db))

    partial = []
    for object in partially_filled:
        partial.append(object)


    return render_template('idsr_reports.html', result=partial)

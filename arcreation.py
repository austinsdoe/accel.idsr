import json
from jsonapi import JSONAPI

jsonapi = JSONAPI()

class ARCREATION(object):

    def create_client(self, **kwargs):

        #kwargs = json.loads(kwargs)

        param = {
            'obj_path': '/Plone/clients',
            'obj_type': 'Client',
            'title': kwargs['reporting_health_facility'],
            'ClientID': kwargs['facility_code']
        }
        return jsonapi.create(**param)

    def create_client_full(self, **kwargs):

        param = {
            'obj_path': '/Plone/clients',
            'obj_type': 'Client',
            'title': kwargs['reporting_health_facility'],
            'ClientID': kwargs['facility_code'],
            'PhysicalAddress': {
                'district': kwargs['patient_county_of_residence'],
                'city': kwargs['patient_community_of_residence'],
                'state': kwargs['patient_county_of_residence']
            }
        }
        return jsonapi.create(**param)

    def create_client_contact(self, client_data, **kwargs):
       # kwargs = json.loads(kwargs)
        param = {
            'obj_path': '/Plone/clients/' + client_data['obj_id'],
            'obj_type': 'Contact',
            'Firstname': kwargs['reporting_person_first_name'],
            'Surname': kwargs['reporting_person_last_name'],
        }
        return jsonapi.create(**param)

    def create_reg_patient_full(self, client_data, **kwargs):
        #kwargs = json.loads(kwargs)
        param = {
            'obj_path': '/Plone/patients',
            'obj_type': 'Patient',
            'Firstname':kwargs["patient_first_name"],
            'PrimaryReferrer': client_data['obj_id'],
            'Surname': kwargs['patient_last_name'],
            'Gender': kwargs['patient_gender'],
            'BirthDate': kwargs['patient_date_of_birth'],
            'ClientPatientID': kwargs['patient_record_id'],
            'PhysicalAddress': {
                'district': kwargs['patient_district_of_residence'],
                'state': kwargs['patient_county_of_residence']
            },
            'PatientIdentifiers': [
                {'IdentifierType': 'Head of HouseHold', 'Identifier': kwargs['head_of_household']},
                {'IdentifierType': 'Head of HouseHold Phone Number',
                 'Identifier': kwargs['patient_parent_phone_number']}
            ],
            'MothersName': kwargs['patient_parent_name'],
            'FathersName': kwargs['patient_parent_name']
        }
        return jsonapi.create(**param)

    def create_reg_patient(self, client_data, **kwargs):
        param = {
            'obj_path': '/Plone/patients',
            'obj_type': 'Patient',
            'Firstname': kwargs['patient_first_name'],
            'PrimaryReferrer': client_data['obj_id'],
            'Surname': kwargs['patient_last_name'],
            'Gender': kwargs['patient_gender'],
            'BirthDate': kwargs['patient_date_of_birth'],
            'ClientPatientID': kwargs['patient_record_id']
        }
        return jsonapi.create(**param)

    def create_analysis_request(self, client_data, client_contact_data, patient_data, **kwargs):
       # kwargs = json.loads(kwargs)
        param = {
            'obj_type': 'AnalysisRequest',
            'Client': 'portal_type:Client|id:'+client_data['obj_id'],
            'SampleType': 'portal_type:SampleType|title:Semen (EVD)',
            'Contact': 'portal_type:Contact|getId:'+client_contact_data['obj_id'],
            'Services:list': 'portal_type:AnalysisService|title:GeneXpert_EVD',
            'SamplingDate': '2016/09/29',
            'Patient': 'portal_type:Patient|catalog_name:bika_patient_catalog|getId:'+patient_data['obj_id']
        }
        return jsonapi.create(**param)

    def update_patient(self, **kwargs):
       # kwargs = json.loads(kwargs)
        param = {
            'obj_path':'/Plone/patient/'+kwargs["bika_patient_id"],
            'PhysicalAddress':{
                'district':kwargs['reporting_district'],
                'state':kwargs['reporting_county']
            },
            'PatientIdentifiers':[
                {'IdentifierType':'Head of HouseHold', 'Identifier':kwargs['head_of_household']},
                {'IdentifierType': 'Head of HouseHold Phone Number',
                 'Identifier': kwargs['patient_parent_phone_number']}
            ],
            'MothersName': kwargs['patient_parent_name'],
            'FathersName': kwargs['patient_parent_name']

        }
        return jsonapi.update(**param)

    def update_client(self, **kwargs):
        #kwargs = json.loads(kwargs)
        param = {
            'obj_path': '/Plone/client/' + kwargs["bika_client_id"],
            'PhysicalAddress': {
                'district': kwargs['patient_county_of_residence'],
                'city': kwargs['patient_community_of_residence'],
                'state': kwargs['patient_county_of_residence']
            }
        }
        return jsonapi.update(**param)

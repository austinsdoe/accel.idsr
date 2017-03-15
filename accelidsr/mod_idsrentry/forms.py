from wtforms import BooleanField, TextField, TextAreaField, PasswordField, validators, HiddenField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf import Form
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices

def getIdsrEntryForm(step):
    if step.lower() == 'a':
        return IdsrEntryStepAForm()
    if step.lower() == 'b':
        return IdsrEntryStepBForm()
    if step.lower() == 'c':
        return IdsrEntryStepCForm()
    if step.lower() == 'd':
        return IdsrEntryStepCForm()
    raise NotImplementedError("No form available for step '%s'" % step)

class AbstractIdsrEntryStepForm(Form):

    step = ''
    submit = SubmitField("Next")

    def getSubsteps(self):
        raise NotImplementedError( "Should have implemented this" )


class IdsrEntryStepAForm(AbstractIdsrEntryStepForm):

    step = 'A'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = SelectField('Reporting District', choices=getDistrictChoices(), validators=[DataRequired(), ])
    facility_name = SelectField('Health Facility Name', choices=getFacilityChoices(), validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepBForm(AbstractIdsrEntryStepForm):

    step = 'B'

    # Step B.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step B.2
    reporting_country = SelectField('Reporting County', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = SelectField('Reporting District', choices=getDistrictChoices(), validators=[DataRequired(), ])
    facility_name = SelectField('Health Facility Name', choices=getFacilityChoices(), validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepCForm(AbstractIdsrEntryStepForm):

    step = 'C'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = TextField('Reporting District', validators=[DataRequired(), ])
    facility_name = TextField('Health Facility Name', validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

class IdsrEntryStepDForm(AbstractIdsrEntryStepForm):

    step = 'D'

    # Step A.1
    reporting_date = DateField('Reporting Date', format='%d/%m/%Y', validators=[DataRequired(), ])
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step A.2
    reporting_country = SelectField('Reporting Country', choices=getCountiesChoices(), validators=[DataRequired(), ])
    reporting_district = TextField('Reporting District', validators=[DataRequired(), ])
    facility_name = TextField('Health Facility Name', validators=[DataRequired(), ])

    def getSubsteps(self):
        return [
            [self.reporting_date, self.facility_code, self.case_id, self.patient_record_id],
            [self.reporting_country, self.reporting_district, self.facility_name]
        ]

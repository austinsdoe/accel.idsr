from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices
from accelidsr.mod_idsrentry.forms import AbstractIdsrEntryStepForm

class IdsrEntryStepAForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step A - Basic Information" from IDSR Form.
    """
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

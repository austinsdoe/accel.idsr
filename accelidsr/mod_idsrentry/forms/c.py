from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry.forms import AbstractIdsrEntryStepForm

class IdsrEntryStepCForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step C - Patient Basic information" from IDSR Form.
    """
    step = 'C'

    # Step C.1
    patient_anonymous = BooleanField('Anonymous Patient')
    patient_firstname = TextField('Patient First Name', validators=[DataRequired(), Length(min=3)])
    patient_middlename = TextField('Patient Middle Name')
    patient_lastname = TextField('Patient Last Name', validators=[DataRequired(), Length(min=3)])
    patient_client_patientid = TextField('Client Patient ID', validators=[DataRequired(), Length(min=3)])
    patient_gender = RadioField('Patient Gender',  default='u', choices=[('u', 'Unknown'), ('m', 'Male'), ('f', 'Female')])
    patient_dateofbirth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired(), ])
    patient_age_years = IntegerField('Patient Age. Years', validators=[DataRequired(), Length(min=4, max=4)])
    patient_age_months = IntegerField('Patient Age. Months', validators=[DataRequired(), Length(min=1, max=2)])
    patient_age_days = IntegerField('Patient Age. Days', validators=[DataRequired(), Length(min=1, max=2)])

    # Step C.2
    patient_county_of_residence = SelectField('Patient County of Residence', choices=getCountiesChoices(), validators=[DataRequired(), ])
    patient_district_of_residence = SelectField('Patient District of Residence', choices=getDistrictChoices(), validators=[DataRequired(), ])
    patient_community_of_residence = TextField('Patient Community of Residence', validators=[DataRequired(), Length(min=3)])

    # Step C.3
    patient_head_of_household = TextField('Head of Household')
    patient_parents_name = TextField('Parents Name (if young)')
    patient_phone_number = TextField('Parent Phone Number', validators=[Length(max=10), ])

    # Step C.4
    patient_cross_border = RadioField('Cross Border in Last Month?',  default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    patient_case_detected_community = RadioField('Case Detected at Community Level?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])


    def getSubsteps(self):
        return [
            [self.patient_anonymous, self.patient_firstname, self.patient_middlename, self.patient_lastname, self.patient_client_patientid, self.patient_gender, self.patient_dateofbirth, self.patient_age_years, self.patient_age_months, self.patient_age_days],
            [self.patient_county_of_residence, self.patient_district_of_residence, self.patient_community_of_residence],
            [self.patient_head_of_household, self.patient_parents_name, self.patient_phone_number],
            [self.patient_cross_border, self.patient_case_detected_community]
        ]

from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField
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
    patient_firstname = TextField('Patient First Name', validators=[DataRequired(), Length(min=3)])
    patient_middlename = TextField('Patient Middle Name')
    patient_lastname = TextField('Patient Last Name', validators=[DataRequired(), Length(min=3)])
    patient_sex = RadioField('Patient Sex',  default='u', choices=[('u', 'Unknown'), ('m', 'Male'), ('f', 'Female')])
    patient_dateofbirth = DateField('Date of Birth', format='%d/%m/%Y', validators=[DataRequired(), ])

    # Step C.2
    patient_county_of_residence = SelectField('County of Residence', choices=getCountiesChoices(), validators=[DataRequired(), ])
    patient_district_of_residence = SelectField('District of Residence', choices=getDistrictChoices(), validators=[DataRequired(), ])
    patient_community_of_residence = TextField('Community of Residence', validators=[DataRequired(), Length(min=3)])

    # Step C.3
    patient_head_of_household = TextField('Head of Household')
    patient_parents_name = TextField('Patient Parents Name')
    patient_phone_number = TextField('Patient Phone Number', validators=[Length(max=10), ])

    # Step C.4
    patient_cross_border = RadioField('Cross Border in Last Month?',  default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    patient_case_detected_community = RadioField('Case Detected at Community Level?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])


    def getSubsteps(self):
        return [
            [self.patient_firstname, self.patient_middlename, self.patient_lastname, self.patient_sex, self.patient_dateofbirth],
            [self.patient_county_of_residence, self.patient_district_of_residence, self.patient_community_of_residence],
            [self.patient_head_of_household, self.patient_parents_name, self.patient_phone_number],
            [self.patient_cross_border, self.patient_case_detected_community]
        ]

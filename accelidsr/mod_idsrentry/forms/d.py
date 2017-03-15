from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getCaseOutcomeChoices
from accelidsr.mod_idsrentry import getCaseClassificationChoices
from accelidsr.mod_idsrentry import getSpecimenTypeChoices
from accelidsr.mod_idsrentry import getAnalysisProfileChoices
from accelidsr.mod_idsrentry.forms import AbstractIdsrEntryStepForm

class IdsrEntryStepDForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step D - Clinical information" from IDSR Form.
    """
    step = 'D'

    # Step D.1
    case_date_of_onset = DateField('Date of Onset', format='%d/%m/%Y', validators=[DataRequired(), ])
    case_date_seen = DateField('Date Seen', format='%d/%m/%Y', validators=[DataRequired(), ])
    case_inout_patient = RadioField('In/Out Patient', choices=[('in', 'In Patient'), ('out', 'Out Patient')])
    case_outcome = RadioField('Outcome', choices=getCaseOutcomeChoices())
    case_classification = SelectField('Classification', choices=getCaseClassificationChoices())

    # Step D.2
    reporting_person_firstname = TextField('Reporting Person First Name', validators=[DataRequired(), Length(min=3)])
    reporting_person_lastname = TextField('Reporting Person Last Name', validators=[DataRequired(), Length(min=3)])
    reporting_person_phone = TextField('Phone Number of Reporting Person', validators=[DataRequired(),])
    sampler_name = TextField('Name of Person Collecting Specimen', validators=[DataRequired(),])
    sampler_phone = TextField('Phone Number of Person Collecting Specimen', validators=[DataRequired(),])

    # Step D.3
    health_worker_comments = TextAreaField('Comments')
    facility_code = TextField('Facility Code', validators=[DataRequired(), Length(max=8)])
    case_id = TextField('Case ID', validators=[Length(max=3), ])
    patient_record_id = TextField('Patient Record ID', validators=[Length(max=8), ])

    # Step D.4
    vaccinated_for_disease = RadioField('Vaccinated for this disease?', default='u', choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])
    number_of_vaccinations = IntegerField('Number of vaccinations')
    date_of_most_recent_vaccination = DateField('Date of most recent vaccination', format='%d/%m/%Y')

    # Step D.5
    date_sampled = DateField('Date of Specimen Collection', format='%d/%m/%Y', validators=[DataRequired(), ])
    date_specimen_sent = DateField('Date of Specimen Sent to Lab', format='%d/%m/%Y', validators=[DataRequired(), ])
    sample_type = SelectField('Specimen Type', choices=getSpecimenTypeChoices())
    analyses_requested = SelectField('Lab Analysis Requested', choices=getAnalysisProfileChoices())

    def getSubsteps(self):
        return [
            # D.1
            [self.case_date_of_onset,
             self.case_date_seen,
             self.case_inout_patient,
             self.case_outcome,
             self.case_classification],

            #D.2
            [self.reporting_person_firstname,
             self.reporting_person_lastname,
             self.reporting_person_phone,
             self.sampler_name,
             self.sampler_phone],

            #D.3
            [self.health_worker_comments],

            #D.3
            [self.vaccinated_for_disease,
             self.number_of_vaccinations,
             self.date_of_most_recent_vaccination],

            #D.4
            [self.date_sampled,
             self.date_specimen_sent,
             self.sample_type,
             self.analyses_requested]
        ]

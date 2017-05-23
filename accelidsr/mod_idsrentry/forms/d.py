from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateTimeField, SelectField, \
                    SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getCaseOutcomeChoices
from accelidsr.mod_idsrentry import getCaseClassificationChoices
from accelidsr.mod_idsrentry import getSpecimenTypeChoices
from accelidsr.mod_idsrentry import getAnalysisProfileChoices
from accelidsr.mod_idsrentry.forms import registerStepForm
from accelidsr.mod_idsrentry.forms.baseform import AbstractIdsrEntryStepForm
from datetime import datetime

STEP = ('D', 'Clinical information')


class IdsrEntryStepD1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step D - Clinical information" from IDSR Form.
    """
    case_date_of_onset = DateTimeField(
        'Date of Onset',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date', 'no_future': '1'})

    case_date_seen = DateTimeField(
        'Date Seen',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date', 'no_future': '1'})

    case_inout_patient = RadioField(
        'In/Out Patient',
        choices=[('in', 'In Patient'),
                 ('out', 'Out Patient'), ('unk', 'Not Indicated')])

    case_outcome = RadioField(
        'Outcome',
        choices=getCaseOutcomeChoices())

    case_classification = SelectField(
        'Classification',
        choices=getCaseClassificationChoices())

    def validate(self):
        """
        Validator of D1 step.
        Checks different fields. In case of any error, adds error message(s)
        to field(s) and returns False.
        :returns: `True` if no errors occur.
        :rtype: boolean
        """
        success = super(IdsrEntryStepD1Form, self).validate()
        failures = 0 if success else 1
        # Date of Onset/seem can't be future date. No need to check format.
        # Already checked by DateTimeField formatter which returns None in case
        # of wrong format. Just add message if empty.
        d_onset = self.case_date_of_onset.data
        if not d_onset:
            self.case_date_of_onset.errors.append("Please enter valid date in \
                DD/MM/YYYY format.")
            failures += 1
        elif d_onset > datetime.now():
            self.case_date_of_onset.errors.append("Date of Onset can't be \
                future date")
            failures += 1

        d_seen = self.case_date_seen.data
        if not d_seen:
            self.case_date_seen.errors.append("Please enter valid date in \
                DD/MM/YYYY format.")
            failures += 1
        elif d_seen > datetime.now():
            self.case_date_seen.errors.append("Date Seen can't be future date")
            failures += 1

        # If eveything is correct, do not allow "Date of Onset" to be after
        # "Date Seen".
        if failures == 0 and d_onset > d_seen:
            self.case_date_of_onset.errors.append("Date of Onset can't be \
                after Date Seen.")
            failures += 1

        return failures == 0


registerStepForm(clazz=IdsrEntryStepD1Form, step=STEP, substep=1)


class IdsrEntryStepD2Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step D - Clinical information" from IDSR Form.
    """
    reporting_person_firstname = TextField(
        'Reporting Person First Name',
        validators=[DataRequired(), Length(min=3)])
    reporting_person_lastname = TextField(
        'Reporting Person Last Name',
        validators=[DataRequired(), Length(min=3)])
    reporting_person_phone = TextField(
        'Phone Number of Reporting Person',
        validators=[DataRequired(), ])
    sampler_name = TextField(
        'Name of Person Collecting Specimen',
        validators=[DataRequired(), ])
    sampler_phone = TextField(
        'Phone Number of Person Collecting Specimen',
        validators=[DataRequired(), ])

registerStepForm(clazz=IdsrEntryStepD2Form, step=STEP, substep=2)


class IdsrEntryStepD3Form(AbstractIdsrEntryStepForm):
    health_worker_comments = TextAreaField(
        'Comments',
        render_kw={'rows': '5', 'cols': '50'})

    facility_code = TextField(
        'Facility Code',
        validators=[DataRequired(), Length(max=12)]) # maxlength was 8

    case_id = TextField(
        'Case ID',
        validators=[Length(max=3), ])

    patient_record_id = TextField(
        'Patient Record ID',
        validators=[Length(max=8), ])

registerStepForm(clazz=IdsrEntryStepD3Form, step=STEP, substep=3)


class IdsrEntryStepD4Form(AbstractIdsrEntryStepForm):
    vaccinated_for_disease = RadioField(
        'Vaccinated for this disease?',
        default='u',
        choices=[('y', 'Yes'), ('n', 'No'), ('u', 'Unknown')])

    number_of_vaccinations = IntegerField(
        'Number of vaccinations',
        validators=[validators.optional(), ])

    date_of_most_recent_vaccination = DateTimeField(
        'Date of most recent vaccination',
        format='%d/%m/%Y',
        render_kw={'input-type': 'date'},
        validators=[validators.optional(), ])

registerStepForm(clazz=IdsrEntryStepD4Form, step=STEP, substep=4)


class IdsrEntryStepD5Form(AbstractIdsrEntryStepForm):
    date_sampled = DateTimeField(
        'Date of Specimen Collection',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date'})

    date_specimen_sent = DateTimeField(
        'Date of Specimen Sent to Lab',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date'})

    sample_type = SelectField(
        'Specimen Type',
        choices=getSpecimenTypeChoices())

    analyses_requested = SelectField(
        'Lab Analysis Requested',
        validators=[DataRequired(), ],
        choices=getAnalysisProfileChoices())

registerStepForm(clazz=IdsrEntryStepD5Form, step=STEP, substep=5)

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

STEP = ('D', 'Clinical information')


class IdsrEntryStepD1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step D - Clinical information" from IDSR Form.
    """
    case_date_of_onset = DateTimeField(
        'Date of Onset',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'type': 'date'})

    case_date_seen = DateTimeField(
        'Date Seen',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'type': 'date'})

    case_inout_patient = RadioField(
        'In/Out Patient',
        choices=[('in', 'In Patient'), ('out', 'Out Patient')])

    case_outcome = RadioField(
        'Outcome',
        choices=getCaseOutcomeChoices())

    case_classification = SelectField(
        'Classification',
        choices=getCaseClassificationChoices())

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
        'Comments')

    facility_code = TextField(
        'Facility Code',
        validators=[DataRequired(), Length(max=8)])

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
        render_kw={'type': 'date'},
        validators=[validators.optional(), ])

registerStepForm(clazz=IdsrEntryStepD4Form, step=STEP, substep=4)


class IdsrEntryStepD5Form(AbstractIdsrEntryStepForm):
    date_sampled = DateTimeField(
        'Date of Specimen Collection',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'type': 'date'})

    date_specimen_sent = DateTimeField(
        'Date of Specimen Sent to Lab',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'type': 'date'})

    sample_type = SelectField(
        'Specimen Type',
        choices=getSpecimenTypeChoices())

    analyses_requested = SelectField(
        'Lab Analysis Requested',
        choices=getAnalysisProfileChoices())

registerStepForm(clazz=IdsrEntryStepD5Form, step=STEP, substep=5)

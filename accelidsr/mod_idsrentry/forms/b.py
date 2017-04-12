from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateTimeField, SelectField, \
                    SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getDiagnosisChoices
from accelidsr.mod_idsrentry.forms import registerStepForm
from accelidsr.mod_idsrentry.forms.baseform import AbstractIdsrEntryStepForm

STEP = ('B', 'Diagnosis information')


class IdsrEntryStepB1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step B - Diagnosis information" from IDSR Form.
    """
    diagnosis = RadioField(
        'Diagnosis or Condition',
        choices=getDiagnosisChoices(),
        validators=[DataRequired(), ])

    diagnosis_other = TextField('Other diagnosis',
        render_kw={'style': 'hidden'})

registerStepForm(clazz=IdsrEntryStepB1Form, step=STEP, substep=1)

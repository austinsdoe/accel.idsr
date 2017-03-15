from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateField, SelectField, \
                    SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getDiagnosisChoices
from accelidsr.mod_idsrentry.forms import AbstractIdsrEntryStepForm

class IdsrEntryStepBForm(AbstractIdsrEntryStepForm):
    """
    Form for "Step B - Diagnosis information" from IDSR Form.
    """
    step = 'B'

    # Step B.1
    diagnosis_or_condition = SelectField('Diagnosis or Condition', choices=getDiagnosisChoices(), validators=[DataRequired(), ])
    other_diagnosis = TextField('Other diagnosis')

    def getSubsteps(self):
        return [
            [self.diagnosis_or_condition, self.other_diagnosis],
        ]

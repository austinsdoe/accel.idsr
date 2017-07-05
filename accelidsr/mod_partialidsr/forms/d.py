from wtforms import SelectField, DateTimeField
from wtforms.validators import DataRequired
from accelidsr.mod_partialidsr.forms import registerStepForm
from accelidsr.mod_partialidsr.forms.baseform import AbstractPartialIdsrStepForm
from accelidsr.mod_idsrentry import getSpecimenTypeChoices
from accelidsr.mod_idsrentry import getAnalysisProfileChoices

STEP = ('D', 'Sample Information')

class PartialIdsrD(AbstractPartialIdsrStepForm):
    """
    Partial Form "Step D- Sample Information".
    """
    date_sampled = DateTimeField(
        'Date of Specimen Collection',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date', 'no_future': '1'})

    sample_type = SelectField(
        'Specimen Type',
        choices=getSpecimenTypeChoices())

    analyses_requested = SelectField(
        'Lab Analysis Requested',
        validators=[DataRequired(), ],
        choices=getAnalysisProfileChoices())

    def validate(self):
        """
        Validates the form by calling `validate` on each field.
        :returns: `True` if no errors occur.
        :rtype: bool
        """
        success = super(PartialIdsrD, self).validate()
        failures = 0 if success else 1
        return failures == 0

registerStepForm(clazz=PartialIdsrD, step=STEP)

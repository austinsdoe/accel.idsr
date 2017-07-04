from wtforms import StringField
from wtforms.validators import DataRequired, Length
from accelidsr.mod_partialidsr.forms import registerStepForm
from accelidsr.mod_partialidsr.forms.baseform import AbstractPartialIdsrStepForm

STEP = ('B', 'Contact Information')


class PartialIdsrB(AbstractPartialIdsrStepForm):
    """
    Partial Form "Step B- Contact Information".
    """
    reporting_person_firstname = StringField(
        'Reporting Person First Name',
        validators=[DataRequired(), Length(min=3)])
    reporting_person_lastname = StringField(
        'Reporting Person Last Name',
        validators=[DataRequired(), Length(min=3)])
    reporting_person_phone = StringField(
        'Phone Number of Reporting Person',
        validators=[DataRequired(),  Length(min=10, max=10)])

    def validate(self):
        """
        Validates the form by calling `validate` on each field. Also checks if
        the value fields match with the values set in other steps or Substeps
        for the current IDSR object. (e.g. County Code must match with the
        county selected in the Reporting County SelectList from step A)

        :returns: `True` if no errors occur.
        :rtype: bool
        """
        success = super(PartialIdsrB, self).validate()
        failures = 0 if success else 1
        return failures == 0

registerStepForm(clazz=PartialIdsrB, step=STEP)

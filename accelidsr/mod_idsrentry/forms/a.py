from wtforms import BooleanField, TextField, TextAreaField, PasswordField, \
                    validators, HiddenField, DateTimeField, SelectField, \
                    SubmitField, RadioField
from wtforms.validators import DataRequired, Email, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices
from accelidsr.mod_idsrentry.validators import DynamicDataValidator
from accelidsr.mod_idsrentry.forms import registerStepForm
from accelidsr.mod_idsrentry.forms.baseform import AbstractIdsrEntryStepForm
from accelidsr import db

STEP = ('A', 'Basic information')


class IdsrEntryStepA1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step A.1 - Basic Information" from IDSR Form.
    """
    reporting_date = DateTimeField(
        'Reporting Date',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'input-type': 'date'})

    county_code = SelectField(
        'Reporting County',
        choices=getCountiesChoices(),
        validators=[DataRequired(), ],)

    reporting_district = SelectField(
        'Reporting District',
        choices=getDistrictChoices(),
        validators=[DataRequired(), DynamicDataValidator(), ],)

    reporting_health_facility = SelectField(
        'Reporting Health Facility',
        choices=getFacilityChoices(),
        validators=[DataRequired(), DynamicDataValidator(), ])

    facility_code = TextField(
        'Facility Code',
        validators=[DataRequired(), Length(max=12)]) # maxlength was 8

    case_id = TextField(
        'Case ID',
        validators=[DataRequired(), Length(max=8), ])

    def initFromIdsrObject(self, idsrobj=None):
        super(IdsrEntryStepA1Form, self).initFromIdsrObject(idsrobj)
        # We need first to assign the choices to fields their values are
        # rendered dynamically
        county = self.county_code.data
        district = self.reporting_district.data
        districts = getDistrictChoices(county)
        facilities = getFacilityChoices(county, district)
        self.reporting_district.choices = districts
        self.reporting_health_facility.choices = facilities

    def validate(self):
        """
        Validates the form by calling `validate` on each field. Also checks if
        the value fields match with the values set in other steps or Substeps
        for the current IDSR object. (e.g. County Code must match with the
        county selected in the Reporting County SelectList from step A.2)

        :returns: `True` if no errors occur.
        :rtype: bool
        """
        success = super(IdsrEntryStepA1Form, self).validate()
        failures = 0 if success else 1
        return failures == 0


registerStepForm(clazz=IdsrEntryStepA1Form, step=STEP, substep=1)

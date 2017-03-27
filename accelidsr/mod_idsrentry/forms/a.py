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

STEP = ('A', 'Basic information')


class IdsrEntryStepA1Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step A.1 - Basic Information" from IDSR Form.
    """
    reporting_date = DateTimeField(
        'Reporting Date',
        format='%d/%m/%Y',
        validators=[DataRequired(), ],
        render_kw={'type': 'date'})

    county_code = TextField(
        'County Code',
        validators=[DataRequired(), Length(max=8)])

    facility_code = TextField(
        'Facility Code',
        validators=[DataRequired(), Length(max=8)])

    case_id = TextField(
        'Case ID',
        validators=[Length(max=3), ])

registerStepForm(clazz=IdsrEntryStepA1Form, step=STEP, substep=1)


class IdsrEntryStepA2Form(AbstractIdsrEntryStepForm):
    """
    Form for "Step A.2 - Basic Information" from IDSR Form.
    """
    reporting_country = SelectField(
        'Reporting Country',
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

    def initFromIdsrObject(self, idsrobj=None):
        super(IdsrEntryStepA2Form, self).initFromIdsrObject(idsrobj)
        # We need first to assign the choices to fields their values are
        # rendered dynamically
        county = self.reporting_country.data
        district = self.reporting_district.data
        districts = getDistrictChoices(county)
        facilities = getFacilityChoices(county, district)
        self.reporting_district.choices = districts
        self.reporting_health_facility.choices = facilities

registerStepForm(clazz=IdsrEntryStepA2Form, step=STEP, substep=2)

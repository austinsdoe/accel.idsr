from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length
from accelidsr.mod_idsrentry import getCountiesChoices
from accelidsr.mod_idsrentry import getDistrictChoices
from accelidsr.mod_idsrentry import getFacilityChoices
from accelidsr.mod_idsrentry.validators import DynamicDataValidator
from accelidsr.mod_partialidsr.forms import registerStepForm
from accelidsr.mod_partialidsr.forms.baseform import AbstractPartialIdsrStepForm

STEP = ('A', 'Basic information')


class PartialIdsrA(AbstractPartialIdsrStepForm):
    """
    Partial Form "Step A- Basic Information".
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

    facility_code = StringField(
        'Facility Code',
        validators=[DataRequired(), Length(max=12)])

    case_id = StringField(
        'Case ID',
        validators=[DataRequired(), Length(max=8), ])

    def initFromIdsrObject(self, idsrobj=None):
        super(PartialIdsrA, self).initFromIdsrObject(idsrobj)
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
        success = super(PartialIdsrA, self).validate()
        failures = 0 if success else 1
        return failures == 0

registerStepForm(clazz=PartialIdsrA, step=STEP)

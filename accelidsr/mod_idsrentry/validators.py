from wtforms.validators import ValidationError


class DynamicDataValidator(object):
    """
    Validator that is used for the generation of fields that requires dynamic
    loading of data via ajax calls. As an example, a SelectionList field that
    must be populated from scratch with fresh values after the value of a
    Selection List populated with counties changes.
    """
    field_flags = ('dynamic',)

    def __call__(self, form, field):
        """
        Validates if the field to which this validator has been assigned has
        a value assigned (Required), otherwise, raises a ValidationError
        :param form: the form in which the field is loaded
        :type form: flask_wtf.FlaskForm
        :param field: the field to which this validator has been assigned.
        :type field: wtforms.SelectionList, wtforms.TextField, etc.
        """
        value = field.data
        if not value:
            return ValidationError(self.message)

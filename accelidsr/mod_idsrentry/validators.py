from wtforms.validators import ValidationError

class DynamicDataValidator(object):
    field_flags = ('dynamic',)

    def __call__(self, form, field):
        value = field.data
        if not value:
            return ValidationError(self.message)

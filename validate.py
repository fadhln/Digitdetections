from marshmallow import Schema, fields, ValidationError, validates

class InputSchema(Schema):
    # url = fields.Url(required=True)
    
    url = fields.Url(required=True, allow_none=False)
    details = fields.String(required=True, allow_none=False)

    @validates('details')
    def validate_details(self, value):
        if(value==""):
            raise ValidationError("details cannot be empty")


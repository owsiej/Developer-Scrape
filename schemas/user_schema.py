from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True,
                          validate=validate.Regexp(regex=r"^[\wA-Z0-9]{1,8}$",
                                                   error="Login can have a maximum 8 chars with no special chars "
                                                         "available."))
    password = fields.Str(required=True,
                          validate=validate.Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])['
                                                         r'A-Za-z\d@$!#%*?&_]{6,15}$',
                                                   error="Password must have 6 to 15 characters with at least one "
                                                         "capital letter, one small letter, one number and one "
                                                         "special character."))

class TypeGuesserException(Exception):
    pass


class DataTypeNotSupported(TypeGuesserException):
    pass


class InvalidDecimalType(TypeGuesserException):
    pass

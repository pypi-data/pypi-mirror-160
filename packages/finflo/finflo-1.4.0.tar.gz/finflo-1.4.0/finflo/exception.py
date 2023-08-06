
## BASIC EXCEPTION CLASSES 


class ActionNotFound(Exception):
    pass


class TypeDoesNotExist(Exception):
    pass

class TypeEmpty(Exception):
    pass

class ModelNotfound(Exception):
    pass

class MoreThanOneModel(Exception):
    pass

class IDError(Exception):
    pass

class SignLengthError(Exception):
    pass


class TransitionNotAllowed(Exception):
    pass
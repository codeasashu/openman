class OpenmanException(Exception):
    pass

class RequestParserException(OpenmanException):
    pass

class ResponseParserException(OpenmanException):
    pass

class CollectionParserException(OpenmanException):
    pass

class FolderParserException(OpenmanException):
    pass

class RequestItemParserException(OpenmanException):
    pass
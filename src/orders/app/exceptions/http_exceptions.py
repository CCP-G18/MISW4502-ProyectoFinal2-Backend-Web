from werkzeug.exceptions import HTTPException

class BadRequestError(HTTPException):
    code:int = 400
    description:str = "Solicitud incorrecta"

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__()

class UnauthorizedError(HTTPException):
    code:int = 401
    description:str = "No autorizado"

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__()

class ForbiddenError(HTTPException):
    code:int = 403
    description:str = "Prohibido"

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__()

class NotFoundError(HTTPException):
    code:int = 404
    description:str = "Recurso no encontrado"

    def __init__(self, description=None):
        if description:
            self.description = description
        super().__init__()
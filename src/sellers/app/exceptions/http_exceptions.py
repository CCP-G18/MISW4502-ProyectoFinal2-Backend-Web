from werkzeug.exceptions import HTTPException

class BadRequestError(HTTPException):
  code: int = 400
  description: str = "Solicitud Incorrecta"

  def __init__(self, description=None):
    if description:
      self.description = description
    super().__init__()
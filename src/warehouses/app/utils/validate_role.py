from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.response_util import format_response

def validate_role(role_required):
  def decorator(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
      verify_jwt_in_request()
      claims = get_jwt()
      if claims.get("role") in role_required:
        return fn(*args, **kwargs)
      else:
        return format_response("error", 403, error="No posee los permisos necesarios para acceder a este recurso", message="No tiene los permisos necesarios para acceder a este recurso")
    return wrapper
  return decorator

from flask_jwt_extended import JWTManager
from app.utils.response_util import format_response

jwt = JWTManager()

def init_jwt(app):
  jwt.init_app(app)
  @jwt.unauthorized_loader
  def custom_unauthorized_response(err):
    return format_response("error", 401, error="No se proporcionó un token de autenticación")

  # Personalizar error cuando el token es inválido o expirado
  @jwt.invalid_token_loader
  def custom_invalid_token_response(err):
    return format_response("error", 401, error="Token inválido")

  @jwt.expired_token_loader
  def custom_expired_token_response(jwt_header, jwt_payload):
    return format_response("error", 401, error="El token ha expirado")
import uuid
import re
from app.repositories.user_repository import UserRepository
from app.exceptions.http_exceptions import BadRequestError, NotFoundError, UnauthorizedError, ForbiddenError
from app.models.user_model import User
from app.models.user_model import StatusEnum

def validate_uuid(id):
    try:
        uuid.UUID(id, version=4)
        return True
    except ValueError:
        return False
    
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

class UserService:
    @staticmethod
    def get_all():
        users = UserRepository.get_all()
        if not users:
            raise ValueError("No hay usuarios registrados")
        return users

    @staticmethod
    def get_by_id(user_id):
        if not validate_uuid(user_id):
            raise BadRequestError("El formato del id del producto no es correcto")
            
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        return user
    
    @staticmethod
    def get_by_id_and_status(user_id):
        if not validate_uuid(user_id):
            raise BadRequestError("El formato del id del producto no es correcto")
            
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        if user.status == StatusEnum.BLOCKED:
            raise ForbiddenError("Tu cuenta ha sido bloqueada. Contacta al soporte del G18 para más información.")
        return user

    @staticmethod
    def get_by_email(email):
        if is_valid_email(email) is False:
            raise BadRequestError("El email no es válido")
        return UserRepository.get_by_email(email)

    @staticmethod
    def create(user_data):
        if not user_data.get("name"):
            raise BadRequestError("El nombre es requerido")
        if not user_data.get("lastname"):
            raise BadRequestError("El apellido es requerido")
        if not user_data.get("password"):
            raise BadRequestError("La contraseña es requerida")
        if not user_data.get("email"):
            raise BadRequestError("El email es requerido")
        if is_valid_email(user_data.get("email")) is False:
            raise BadRequestError("El email no es válido")
        if UserRepository.get_by_email(user_data["email"]):
            raise BadRequestError("El email ya está registrado")
        
        user = User(name=user_data["name"], lastname=user_data["lastname"], email=user_data["email"], password=user_data["password"])
        return UserRepository.create(user)
    
    @staticmethod
    def update_status(user_id, user_data):
        if not validate_uuid(user_id):
            raise BadRequestError("El formato del id del producto no es correcto")
        if user_data.get("status") is None:
            raise BadRequestError("El estado es requerido")
        
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundError("Usuario no encontrado")
        
        user.status = user_data["status"]
        UserRepository.update(user)
        return user
    
    @staticmethod
    def check_credentials(user_data):
        if not user_data.get("username"):
            raise BadRequestError("El username es requerido")
        if not user_data.get("password"):
            raise BadRequestError("La contraseña es requerida")
        
        user = UserRepository.get_by_email(user_data["username"]) or UserRepository.get_by_username(user_data["username"])
        if not user or not user.check_password(user_data["password"]):
            raise UnauthorizedError("Credenciales inválidas")
        
        if user.status == "blocked":
            raise ForbiddenError("Tu cuenta ha sido bloqueada. Contacta al soporte del G18 para más información.")
        if user.status == "inactive":
            raise ForbiddenError("Tu cuenta está inactiva. Contacta al soporte del G18 para más información.")
        
        return user
    
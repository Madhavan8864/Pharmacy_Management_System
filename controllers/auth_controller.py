from models.user_model import UserModel

class AuthController:
    @staticmethod
    def login_user(username, password):
        user = UserModel.get_user_by_username(username)
        if user and user['password'] == password:
            return user
        return None
    
    @staticmethod
    def register_user(username, password, role='staff'):
        existing_user = UserModel.get_user_by_username(username)
        if existing_user:
            return None
        return UserModel.create_user(username, password, role)
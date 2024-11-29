from database import Database
class AuthError(Exception):
    pass
class Auth:
    def __init__(self, db: Database):
        self.db = db

    def register(self, username, password):
        return self.db.register_user(username, password)

    def login(self, username, password):
        return self.db.login_user(username, password)
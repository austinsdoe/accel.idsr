from werkzeug.security import check_password_hash, generate_password_hash

class User():
    """
    Class that represents a user
    """
    def __init__(self, id, username, role):
        """
        Initializes the User object
        :param id: the unique identifier of the user
        :type id: string
        :param username: the username of the user
        :type username: string
        :param role: the role of the user
        :type role: string
        """
        self.id = id
        self.username = username
        self.role = role

    def is_admin(self):
        return self.role == 'admin'

    def get_username(self):
        return self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

    @staticmethod
    def generate_hash(password):
        return generate_password_hash(password)

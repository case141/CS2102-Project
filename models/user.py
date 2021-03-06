from flask_login import UserMixin
from db import user_queries
from werkzeug.security import check_password_hash


class User(UserMixin):

    def __init__(self, id, username, email, name, password_hash, phone_no=None):
        self.id = id
        self.username = username
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.phone_no = phone_no

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_user_info(self, username, name, email, phone_no):
        """
        This method uses named arguments, all of which are optional. Send in an argument with the keyword name and
        this method will only update that part of the user.
        :return:
        """
        user_queries.update_user_info(username, name, email, phone_no)

    def create_user(self):
        """
        Creates a user by inserting that user into the table using the attributes of the User object
        :return:
        """
        user_queries.insert_user(self.username, self.email, self.name, self.password_hash, self.phone_no)

    def change_password(self, new_password):
        """
        Changes the old user password to the new one
        :return: true if update is successful, false otherwise
        """
        return user_queries.update_user_password(self.username, new_password)


# Keep only update and insert queries inside the User class for the convenience of using the User attributes.
# while other queries are kept outside since you don't require the User attributes for that.
def get_user_by_id(user_id):
    row = user_queries.get_user_by_id(int(user_id))
    if row is None:
        return None
    return User(**row)


def get_user_by_username(username):
    row = user_queries.get_user_by_username(username)
    if row is None:
        return None
    return User(**row)


def get_users():
    return user_queries.retrieve_users()
import os
from src.Model.DataBase.MyDB.exceptions.DataBaseExceptions import SignInError, SignUpError
from DataBase import DbInterface

PATH = "/Users/ammar/Desktop/Users"


class User:

    def __init__(self, user_name, password, user_space=None):
        self.name = user_name
        self.space = user_space
        self.password = password      # see later if needed

    def get_name(self):
        return self.name

    def get_space(self):
        return self.space

    def get_password(self):
        return self.password


class SignUp:

    def __init__(self, new_user_name, new_password):
        self.user = None
        self.name = new_user_name
        self.password = new_password

    def create_user(self):
        database = DbInterface().get_db()
        space = os.path.join(PATH, self.name)
        new_user = User(self.name, self.password, space)
        database.add_user_in_db(new_user)
        self.create_user_space(space)
        database.close_db()
        self.user = new_user    # should not be here

    def try_create_user(self):
        try:
            self.create_user()      # add a double password check before creating new user
            print("User is added :", self.name)
            return True
        except SignUpError as error:
            print(error.msg)
        except FileExistsError as er:
            print("User exists")
        return False

    def create_user_space(self, space):
        os.mkdir(space)

    def get_user(self):
        return self.user


class SignIn:

    def __init__(self, user_name, password):
        self.user = None
        self.name = user_name
        self.password = password

    def get_user_from_db(self):
        database = DbInterface().get_db()
        user = database.get_user(self)
        return User(user[0], user[1], user[2])

    def try_get_user(self):
        try:
            user = self.get_user_from_db()
            print("success  = ", user.get_space())
            self.user = user    # should not be here
            return True
        except SignInError as error:
            print(error.msg)
        return False

    def get_name(self):
        return self.name

    def get_password(self):
        return self.password

    def get_user(self):
        return self.user


if __name__ == '__main__':

    print("Hello admin !")
    s = SignUp("Sania", "hasan")
    s.try_create_user()

    a = SignIn("Sania", "asan")
    a.try_get_user()



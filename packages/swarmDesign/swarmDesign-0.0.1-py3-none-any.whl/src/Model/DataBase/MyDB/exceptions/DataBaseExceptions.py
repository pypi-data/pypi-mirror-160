
class DataBaseError(Exception):
    pass


class SignUpError(DataBaseError):
    def __init__(self, msg):
        self.msg = msg


class SignInError(DataBaseError):

    def __init__(self, msg):
        self.msg = msg


if __name__ == '__main__':

    try:
        raise (SignInError("Existing user"))
    except SignInError as error:
        print(error.msg)

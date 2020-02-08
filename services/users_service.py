import sys
sys.path.append('../entity')

from users import Users

class UsersService:

    @staticmethod
    def addUser(username, email, password):
        user = Users(username,email, password)
        user.save()
        return user

    @classmethod
    def registerUser(cls,username, email, password, password2):
        if password != password2 :
            raise ValueError('Password not match')
        return cls.addUser(username, email,password2)

import sys
sys.path.append("../utils")

from clcrypto import password_hash
from config import DB_NAME
from sql_utils_class import SqlUtils

class Users:

    def __init__(self, username, password, email):
        self._id = -1
        self.username = username
        self.hashed_password  = password
        self.email = email

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    @hashed_password.setter
    def hashed_password(self, newPass):
        self._hashed_password = password_hash(newPass)


    #### METHODS ####
    def save(self):
        if self._id == -1:
            sql = f'''
                Insert into users (username, email, hashed_password)
                VALUES (%s, %s, %s)
            '''
            params = (self.username, self.email,self._hashed_password )
            newId = SqlUtils.execute_insert_sql(DB_NAME,sql, params)
            if newId:
                self._id = newId
            else:
                raise IOError('Did not saved into DB')
        else:
            sql = f'''
                Update users set username = %s, email = %s, hashed_password = %s
                WHERE id = %s
            '''
            params = (self.username,self.email, self._hashed_password, self._id)
            SqlUtils.execute_sql(DB_NAME,sql, params)

    @classmethod
    def loadById(cls,id):
        sql = f'''
            Select id, username, email, hashed_password From users WHERE id = %s
        '''
        params = (id,)
        data = SqlUtils.execute_sql(DB_NAME, sql, params)
        if data and data[0]:
            return cls._dbRow2User(data[0])
        else:
            return None

    @classmethod
    def loadAll(cls):
        sql = f'Select id, username, email, hashed_password From users'
        data = SqlUtils.execute_sql(DB_NAME, sql)
        result = []
        if data:
            for u in data:
                result.append(cls._dbRow2User(u))
            return result
        else:
            return []

    @classmethod
    def _dbRow2User(cls, rowData):
        user = cls(rowData['username'], rowData['hashed_password'], rowData['email'])
        user._hashed_password = rowData['hashed_password']
        user._id = rowData['id']
        return user
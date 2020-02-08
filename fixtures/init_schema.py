import sys

sys.path.append('../utils')

from sql_utils_class import SqlUtils
from config import DB_NAME

# CREATE DB
SqlUtils.create_db(DB_NAME)

# CRATE TABLE USERS
SQL_USERS = '''
    Create table users (
        id serial primary key ,
        username varchar(255),
        email varchar (255) unique ,
        hashed_password  varchar(80)
    );
'''
try:
    SqlUtils.execute_sql(DB_NAME, SQL_USERS)
except:
    print("Table users already exist")

# CREATE ANOTHER TABLE
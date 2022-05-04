import os

# CONFIG SECTION
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY')
    REGISTERED_USERS = {
    'grady.dickerson04@gmail.com' : {'name':'Grady','password':'abc123'}
    }

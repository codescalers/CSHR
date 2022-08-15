 
from server.cshr.models.users import User
 
from django.contrib.auth.hashers import check_password

def get_user_by_id(id: str) -> User:
    """Return user who have the same id"""
    try:
        return User.objects.get(id=int(id))
    except:
        return None

def get_user_by_email_for_login(email: str) -> User:
    """Return user who have the same email"""
    try:
        return User.objects.get(email=email)
    except:
        return None

def success_login_user(email, password) -> User:
    """Return user who have the same email and password"""
 
    user = User.objects.get(email=email)
   
    if check_password(password, user.password):
            return user
    return None

 
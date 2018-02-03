"""
User authentication for the accounts of the Superlists app
"""

from accounts.models import User
from accounts.models import Token

class PasswordlessAuthenticationBackend(object):
    """
    Class that handelsthe passwordless authentication of users via e-mail links andtokens
    """
    def authenticate(self, uid):
        """
        authenticate the user with the token `uid`
        """
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        """
        returns the User database object for the `email`.
        If no user with that `email` exists it returns none.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

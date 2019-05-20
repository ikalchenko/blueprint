from ..validators import Validator, NotBlank, Unique, MinLength, Alphanumeric
from .models import Task


class NewUserValidator(Validator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rules = {
            'first_name': [NotBlank()],
            'last_name': [NotBlank()],
            'email': [NotBlank(), Unique(model=User, column=User.email)],
            'password': [NotBlank(), Alphanumeric(), MinLength(length=8)]
        }

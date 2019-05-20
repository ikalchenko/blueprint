from ..validators import Validator, NotBlank, MinLength


class NewTripValidator(Validator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rules = {
            'title': [NotBlank(), MinLength(length=2)],
            'country': [NotBlank(), MinLength(length=2)],
            'city': [NotBlank(), MinLength(length=2)],
            'date': [NotBlank()]
        }

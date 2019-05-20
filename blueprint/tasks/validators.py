from ..validators import Validator, NotBlank, MinLength


class NewTaskValidator(Validator):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rules = {
            'title': [NotBlank(), MinLength(length=2)],
        }

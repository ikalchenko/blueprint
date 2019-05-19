from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, **kwargs):
        self.field_values = kwargs
        self.errors = []
        self.valid = True

    def is_valid(self):
        for field, validators in self.rules.items():
            for validator in validators:
                validator.set_field_and_value(field, self.field_values[field])
                validation_result = validator.validate()
                self.valid = False if self.valid and not validation_result else True
                self.errors.extend(validator.get_errors())
        return self.valid


class BaseValidationCase(ABC):

    def __init__(self):
        self._field = None
        self._value = None
        self._errors = []

    def set_field_and_value(self, field, value):
        self._field = field
        self._value = value

    def get_errors(self):
        return self._errors

    @abstractmethod
    def validate(self):
        pass


class NotBlank(BaseValidationCase):
    def validate(self):
        trimmed_value = self._value.strip()
        validation_result = trimmed_value != ''
        if not validation_result:
            self._errors.append(f'{self._field} should not be blank')
        return validation_result


class MinLength(BaseValidationCase):
    def __init__(self, length):
        super().__init__()
        self.length = length

    def validate(self):
        validation_result = len(self._value) >= self.length
        if not validation_result:
            self._errors.append(f'{self._field} minimal length is {str(self.length)} symbols')
        return validation_result


class Alphanumeric(BaseValidationCase):
    def validate(self):
        has_digit = False
        has_letter = False
        validation_result = False
        for char in self._value:
            if not has_digit and char.isdigit():
                has_digit = True
            if not has_letter and char.isalpha():
                has_letter = True
            if has_letter and has_digit:
                validation_result = True
                break
        if not validation_result:
            self._errors.append(f'{self._field} should contain both letters and numbers')
        return validation_result


class Unique(BaseValidationCase):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def validate(self):
        validation_result = not await self.model.query.get({self._field: self._value})
        if not validation_result:
            self._errors.append(f'{self._field} should be unique')
        return validation_result

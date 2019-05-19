from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, **kwargs):
        self.field_values = kwargs
        self.errors = []
        self.validation_results = []

    async def is_valid(self):
        for field, validators in self.rules.items():
            for validator in validators:
                validator.set_field_and_value(field, self.field_values[field])
                validation_result = await validator.validate()
                self.validation_results.append(validation_result)
                self.errors.extend(validator.get_errors())
        return all(self.validation_results)


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
    async def validate(self):
        pass


class NotBlank(BaseValidationCase):
    async def validate(self):
        trimmed_value = self._value.strip()
        validation_result = trimmed_value != ''
        if not validation_result:
            self._errors.append(f'{self._field} should not be blank')
        return validation_result


class MinLength(BaseValidationCase):
    def __init__(self, length):
        super().__init__()
        self.length = length

    async def validate(self):
        validation_result = len(self._value) >= self.length
        if not validation_result:
            self._errors.append(f'{self._field} minimal length is {str(self.length)} symbols')
        return validation_result


class Alphanumeric(BaseValidationCase):
    async def validate(self):
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
    def __init__(self, model, column):
        super().__init__()
        self.model = model
        self.column = column

    async def validate(self):
        user = await self.model.query.where(self.column == self._value).gino.first()
        if user:
            self._errors.append(f'{self._field} should be unique')
        return not user

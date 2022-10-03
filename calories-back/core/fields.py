from django.db import models
from django_case_insensitive_field import (
    CaseInsensitiveFieldMixin as LowerCaseCaseInsensitiveFieldMixin,
)


class CIEmailField(LowerCaseCaseInsensitiveFieldMixin, models.EmailField):
    pass

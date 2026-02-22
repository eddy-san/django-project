from typing import Protocol, Iterable
from .models import Form, Submission

class FormRepository(Protocol):
    def get_active_by_slug(self, slug: str) -> Form: ...

class SubmissionRepository(Protocol):
    def create_for_form(self, form: Form, values_by_field: dict) -> Submission: ...
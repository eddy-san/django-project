import os
from ..persistence.repositories import FormRepository, SubmissionRepository
from ..persistence.repositories_orm import DjangoOrmFormRepository, DjangoOrmSubmissionRepository

def _backend() -> str:
    return os.getenv("PERSISTENCE_BACKEND", "django-orm").lower()

def get_form_repo() -> FormRepository:
    b = _backend()
    if b == "django-orm":
        return DjangoOrmFormRepository()
    raise ValueError(f"Unknown persistence backend: {b}")

def get_submission_repo() -> SubmissionRepository:
    b = _backend()
    if b == "django-orm":
        return DjangoOrmSubmissionRepository()
    raise ValueError(f"Unknown persistence backend: {b}")
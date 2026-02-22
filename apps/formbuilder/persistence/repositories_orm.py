from django.db import transaction
from .models import Form, Submission

class DjangoOrmFormRepository:
    def get_active_by_slug(self, slug: str) -> Form:
        return (
            Form.objects
            .prefetch_related("questions__choices")
            .get(slug=slug, is_active=True)
        )


class DjangoOrmSubmissionRepository:
    @transaction.atomic
    def create_for_form(self, form: Form, values_by_field: dict) -> Submission:
        sub = Submission.objects.create(form=form)

        # Whitelist: nur Felder, die es im Model gibt
        allowed = {f.name for f in Submission._meta.get_fields()}

        for field, value in values_by_field.items():
            if field in allowed:
                setattr(sub, field, value)

        sub.save()
        return sub
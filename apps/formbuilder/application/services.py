from datetime import date
from ..infrastructure.repo_factory import get_form_repo, get_submission_repo

def load_form(slug: str):
    return get_form_repo().get_active_by_slug(slug)

def validate_and_submit(form, raw_post: dict):
    """
    Validiert alle Fragen im Form, gibt (errors, submission_or_none, values) zurück.
    Speichert nur Codes/Jahr in Submission-Spalten entsprechend question.db_field.
    """
    errors = {}
    values = {}
    cleaned_by_field = {}

    current_year = date.today().year

    for q in form.questions.all():
        key = f"q{q.id}"
        raw = (raw_post.get(key) or "").strip()
        values[key] = raw

        if q.required and raw == "":
            errors[key] = "Pflichtfeld."
            continue

        if raw == "":
            cleaned_by_field[q.db_field] = None
            continue

        if q.qtype == "YEAR_4":
            try:
                y = int(raw)
                if y < 1900 or y > current_year:
                    errors[key] = f"Jahr muss zwischen 1900 und {current_year} liegen."
                else:
                    cleaned_by_field[q.db_field] = y
            except ValueError:
                errors[key] = "Bitte ein gültiges Jahr eingeben."

        elif q.qtype == "RADIO_0_5":
            if raw not in {"0", "1", "2", "3", "4", "5"}:
                errors[key] = "Bitte 0 bis 5 wählen."
            else:
                cleaned_by_field[q.db_field] = int(raw)

        else:
            # Für spätere Typen
            cleaned_by_field[q.db_field] = raw

    if errors:
        return errors, None, values

    sub = get_submission_repo().create_for_form(form=form, values_by_field=cleaned_by_field)
    return {}, sub, {}
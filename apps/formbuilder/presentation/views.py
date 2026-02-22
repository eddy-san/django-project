from django.shortcuts import render
from ..application.services import load_form, validate_and_submit

def fill_form(request, slug: str):
    form = load_form(slug)

    submitted = False
    errors = {}
    values = {}

    if request.method == "POST":
        errors, sub, values = validate_and_submit(form, request.POST)
        submitted = sub is not None

    return render(
        request,
        "formbuilder/fill_form.html",
        {
            "form_obj": form,
            "errors": errors,
            "values": values,
            "submitted": submitted,
        },
    )
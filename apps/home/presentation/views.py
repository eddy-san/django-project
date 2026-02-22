from datetime import date
from django.shortcuts import render


def index(request):
    form = {"birth_year": "", "depressed": "0", "sleep": "0"}
    errors = {}
    submitted = None

    if request.method == "POST":
        birth_year_raw = request.POST.get("birth_year", "").strip()
        depressed_raw = request.POST.get("depressed", "0").strip()
        sleep_raw = request.POST.get("sleep", "0").strip()

        form = {
            "birth_year": birth_year_raw,
            "depressed": depressed_raw,
            "sleep": sleep_raw,
        }

        # --- Birth year validation ---
        year = None
        if not birth_year_raw:
            errors["birth_year"] = "Bitte Geburtsjahr angeben."
        else:
            try:
                year = int(birth_year_raw)
                current_year = date.today().year
                if year < 1900 or year > current_year:
                    errors["birth_year"] = (
                        f"Bitte ein gültiges Jahr zwischen 1900 und {current_year} eingeben."
                    )
            except ValueError:
                errors["birth_year"] = "Bitte ein gültiges Jahr eingeben."

        # --- Scale validation ---
        def validate_scale(field_name, raw_value):
            try:
                v = int(raw_value)
                if v < 0 or v > 5:
                    errors[field_name] = "Wert muss zwischen 0 und 5 liegen."
                return v
            except Exception:
                errors[field_name] = "Bitte eine Zahl zwischen 0 und 5 wählen."
                return 0

        depressed_v = validate_scale("depressed", depressed_raw)
        sleep_v = validate_scale("sleep", sleep_raw)

        if not errors:
            submitted = {
                "birth_year": year,
                "depressed": depressed_v,
                "sleep": sleep_v,
            }

    return render(
        request,
        "home/index.html",
        {
            "form": form,
            "errors": errors,
            "submitted": submitted,
            "scale": range(0, 6),
        },
    )
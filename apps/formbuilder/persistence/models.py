from django.db import models

class Form(models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    class QuestionType(models.TextChoices):
        YEAR_4DIGIT = "YEAR_4", "Year (4-digit)"
        RADIO_0_5 = "RADIO_0_5", "Radio (0..5)"

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    order = models.PositiveIntegerField(default=1)

    text = models.CharField(max_length=400)
    help_text = models.CharField(max_length=400, blank=True)

    qtype = models.CharField(max_length=32, choices=QuestionType.choices)
    required = models.BooleanField(default=True)

    # Mapping auf "DB-Spalte"/Feldname in Submission (z.B. birth_year, depressed, sleep)
    db_field = models.SlugField(max_length=64)

    class Meta:
        unique_together = [("form", "order")]
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.form.slug} #{self.order} -> {self.db_field}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    value = models.PositiveSmallIntegerField()  # 0..5
    label = models.CharField(max_length=200)    # "gar nicht", "etwas", ...

    class Meta:
        unique_together = [("question", "value")]
        ordering = ["value"]

    def __str__(self) -> str:
        return f"{self.value}: {self.label}"


class Submission(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="submissions")
    created_at = models.DateTimeField(auto_now_add=True)

    # Beispiel-Spalten (später erweiterbar)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    depressed = models.PositiveSmallIntegerField(null=True, blank=True)  # 0..5
    sleep = models.PositiveSmallIntegerField(null=True, blank=True)      # 0..5

    def __str__(self) -> str:
        return f"{self.form.slug} @ {self.created_at:%Y-%m-%d %H:%M}"
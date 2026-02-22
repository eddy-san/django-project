from django.contrib import admin
from .persistence.models import Form, Question, Choice, Submission

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ("slug", "title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("slug", "title")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("form", "order", "qtype", "db_field", "required", "text")
    list_filter = ("form", "qtype", "required")
    inlines = [ChoiceInline]

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("form", "created_at", "birth_year", "depressed", "sleep")
    list_filter = ("form",)
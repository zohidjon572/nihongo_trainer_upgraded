from django.contrib import admin
from .models import AnswerChoice, ConversationStep, Scenario, UserProgress, UserStepAnswer


class ConversationStepInline(admin.TabularInline):
    model = ConversationStep
    extra = 1
    fields = ("order", "speaker", "japanese_text", "romaji", "translation", "answer_type", "correct_answer_text", "hint")
    ordering = ("order",)


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 2
    fields = ("text", "is_correct")


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ("emoji", "title", "category", "level", "is_active", "total_steps", "created_by", "updated_at")
    list_filter = ("level", "category", "is_active")
    search_fields = ("title", "description")
    inlines = [ConversationStepInline]
    fieldsets = (
        ("Asosiy ma'lumot", {"fields": ("title", "description", "level", "category", "emoji", "estimated_minutes", "is_active")}),
        ("Meta", {"fields": ("created_by",)}),
    )
    readonly_fields = ("created_by",)

    def save_model(self, request, obj, form, change):
        if not obj.pk and not obj.created_by_id:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ConversationStep)
class ConversationStepAdmin(admin.ModelAdmin):
    list_display = ("scenario", "order", "speaker", "japanese_text", "answer_type")
    list_filter = ("scenario", "answer_type")
    search_fields = ("japanese_text", "translation")
    inlines = [AnswerChoiceInline]


@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ("step", "text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text",)


class UserStepAnswerInline(admin.TabularInline):
    model = UserStepAnswer
    extra = 0
    can_delete = False
    readonly_fields = ("step", "given_answer_text", "is_correct", "answered_at")


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "scenario", "attempt_number", "status", "score", "started_at", "completed_at")
    list_filter = ("status", "scenario")
    search_fields = ("user__username", "scenario__title")
    readonly_fields = ("user", "scenario", "attempt_number", "total_steps", "correct_answers", "score", "started_at", "completed_at")
    inlines = [UserStepAnswerInline]
    def has_add_permission(self, request): return False

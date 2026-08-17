from django.conf import settings
from django.db import models
from django.urls import reverse


class Scenario(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Boshlang'ich (N5)"),
        ("intermediate", "O'rta (N4-N3)"),
        ("advanced", "Yuqori (N2-N1)"),
    ]
    CATEGORY_CHOICES = [
        ("daily", "Kundalik hayot"),
        ("travel", "Sayohat"),
        ("school", "Universitet / O'qish"),
        ("work", "Ish / Biznes"),
        ("shopping", "Xarid"),
        ("restaurant", "Restoran / Kafe"),
        ("other", "Boshqa"),
    ]

    title = models.CharField("Sarlavha", max_length=255)
    description = models.TextField("Tavsif", blank=True)
    level = models.CharField("Daraja", max_length=20, choices=LEVEL_CHOICES, default="beginner")
    category = models.CharField("Mavzu", max_length=20, choices=CATEGORY_CHOICES, default="daily")
    emoji = models.CharField("Ikonka (emoji)", max_length=8, default="💬", blank=True)
    estimated_minutes = models.PositiveIntegerField("Taxminiy daqiqa", default=5)
    is_active = models.BooleanField("Faol (talabalarga ko'rinadi)", default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Yaratgan admin/o'qituvchi",
        on_delete=models.SET_NULL, null=True, blank=True, related_name="created_scenarios")
    created_at = models.DateTimeField("Yaratilgan sana", auto_now_add=True)
    updated_at = models.DateTimeField("Yangilangan sana", auto_now=True)

    class Meta:
        verbose_name = "Stsenariy"
        verbose_name_plural = "Stsenariylar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.get_level_display()})"

    def get_absolute_url(self):
        return reverse("trainer:scenario_detail", args=[self.pk])

    @property
    def total_steps(self):
        return self.steps.count()


class ConversationStep(models.Model):
    ANSWER_TYPE_CHOICES = [
        ("choice", "Variantlardan tanlash"),
        ("text", "Matn kiritish (erkin javob)"),
    ]
    scenario = models.ForeignKey(Scenario, verbose_name="Stsenariy", on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField("Tartib raqami", default=1)
    speaker = models.CharField("So'zlovchi", max_length=50, default="AI Sensei")
    japanese_text = models.CharField("Yaponcha matn (savol/replika)", max_length=500)
    romaji = models.CharField("Romaji (talaffuz)", max_length=500, blank=True)
    translation = models.CharField("Tarjima (o'zbekcha/inglizcha)", max_length=500, blank=True)
    answer_type = models.CharField("Javob turi", max_length=10, choices=ANSWER_TYPE_CHOICES, default="choice")
    correct_answer_text = models.CharField("To'g'ri javob matni (matn turi uchun)", max_length=500, blank=True)
    hint = models.CharField("Maslahat (ixtiyoriy)", max_length=255, blank=True)

    class Meta:
        verbose_name = "Dialog qadami"
        verbose_name_plural = "Dialog qadamlari"
        ordering = ["scenario", "order"]
        unique_together = ("scenario", "order")

    def __str__(self):
        return f"{self.scenario.title} - {self.order}. {self.japanese_text[:40]}"


class AnswerChoice(models.Model):
    step = models.ForeignKey(ConversationStep, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField("Variant matni", max_length=255)
    is_correct = models.BooleanField("To'g'ri javobmi?", default=False)

    class Meta:
        verbose_name = "Javob varianti"
        verbose_name_plural = "Javob variantlari"

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} {self.text}"


class UserProgress(models.Model):
    STATUS_CHOICES = [("in_progress", "Jarayonda"), ("completed", "Yakunlangan")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="progress_records")
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name="progress_records")
    attempt_number = models.PositiveIntegerField("Urinish raqami", default=1)
    status = models.CharField("Holat", max_length=15, choices=STATUS_CHOICES, default="in_progress")
    current_step_order = models.PositiveIntegerField("Joriy qadam", default=1)
    total_steps = models.PositiveIntegerField("Jami qadamlar", default=0)
    correct_answers = models.PositiveIntegerField("To'g'ri javoblar soni", default=0)
    score = models.FloatField("Ball (%)", default=0)
    started_at = models.DateTimeField("Boshlangan vaqt", auto_now_add=True)
    completed_at = models.DateTimeField("Tugallangan vaqt", null=True, blank=True)

    class Meta:
        verbose_name = "O'quvchi jarayoni"
        verbose_name_plural = "O'quvchi jarayonlari (Tarix)"
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title} (#{self.attempt_number})"

    def recalculate_score(self):
        self.score = round((self.correct_answers / self.total_steps) * 100, 1) if self.total_steps else 0
        self.save(update_fields=["score"])


class UserStepAnswer(models.Model):
    progress = models.ForeignKey(UserProgress, on_delete=models.CASCADE, related_name="answers")
    step = models.ForeignKey(ConversationStep, on_delete=models.CASCADE, related_name="user_answers")
    given_answer_text = models.CharField("Berilgan javob", max_length=500)
    is_correct = models.BooleanField("To'g'ri javobmi?", default=False)
    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Talaba javobi"
        verbose_name_plural = "Talaba javoblari"
        ordering = ["step__order"]

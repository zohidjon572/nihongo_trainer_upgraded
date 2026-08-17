from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Scenario, ConversationStep, AnswerChoice


class TrainerSmokeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="student", password="StrongPass123!")
        self.scenario = Scenario.objects.create(title="Test", category="daily", level="beginner", is_active=True)
        step = ConversationStep.objects.create(scenario=self.scenario, order=1, japanese_text="こんにちは")
        AnswerChoice.objects.create(step=step, text="こんにちは！", is_correct=True)

    def test_login_and_scenario_list(self):
        self.client.login(username="student", password="StrongPass123!")
        response = self.client.get(reverse("trainer:scenario_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_start_practice(self):
        self.client.login(username="student", password="StrongPass123!")
        response = self.client.get(reverse("trainer:start_scenario", args=[self.scenario.pk]))
        self.assertEqual(response.status_code, 302)

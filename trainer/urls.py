from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "trainer"

urlpatterns = [
    path("", views.scenario_list, name="scenario_list"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="trainer/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="trainer:scenario_list"), name="logout"),
    path("scenario/<int:pk>/", views.scenario_detail, name="scenario_detail"),
    path("scenario/<int:pk>/start/", views.start_scenario, name="start_scenario"),
    path("scenario/<int:pk>/retry/", views.retry_scenario, name="retry_scenario"),
    path("practice/<int:progress_id>/", views.practice, name="practice"),
    path("result/<int:progress_id>/", views.result, name="result"),
    path("history/", views.history, name="history"),
]

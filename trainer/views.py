from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Avg, Count

from .forms import RegisterForm
from .models import AnswerChoice, ConversationStep, Scenario, UserProgress, UserStepAnswer


def register(request):
    if request.user.is_authenticated:
        return redirect("trainer:scenario_list")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Xush kelibsiz! Yapon tilidagi mashqni boshlang.")
        return redirect("trainer:scenario_list")
    return render(request, "trainer/register.html", {"form": form})


@login_required
def scenario_list(request):
    scenarios = Scenario.objects.filter(is_active=True).prefetch_related("steps")
    level = request.GET.get("level", "")
    category = request.GET.get("category", "")
    q = request.GET.get("q", "").strip()
    if level: scenarios = scenarios.filter(level=level)
    if category: scenarios = scenarios.filter(category=category)
    if q: scenarios = scenarios.filter(title__icontains=q) | scenarios.filter(description__icontains=q)
    scenarios = list(scenarios.distinct())
    progress_map = {
        p.scenario_id: p for p in UserProgress.objects.filter(user=request.user).order_by("scenario_id", "-started_at")
    }
    for s in scenarios:
        s.last_progress = progress_map.get(s.pk)
    completed = UserProgress.objects.filter(user=request.user, status="completed")
    context = {
        "scenarios": scenarios, "levels": Scenario.LEVEL_CHOICES, "categories": Scenario.CATEGORY_CHOICES,
        "selected_level": level, "selected_category": category, "query": q,
        "completed_count": completed.count(),
        "avg_score": round(completed.aggregate(v=Avg("score"))["v"] or 0, 1),
    }
    return render(request, "trainer/scenario_list.html", context)


@login_required
def scenario_detail(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk, is_active=True)
    history = UserProgress.objects.filter(user=request.user, scenario=scenario)
    best = history.filter(status="completed").order_by("-score").first()
    return render(request, "trainer/scenario_detail.html", {"scenario": scenario, "history": history, "best": best})


@login_required
def start_scenario(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk, is_active=True)
    in_progress = UserProgress.objects.filter(user=request.user, scenario=scenario, status="in_progress").first()
    if in_progress:
        return redirect("trainer:practice", progress_id=in_progress.pk)
    last = UserProgress.objects.filter(user=request.user, scenario=scenario).order_by("-attempt_number").first()
    progress = UserProgress.objects.create(user=request.user, scenario=scenario,
        attempt_number=(last.attempt_number + 1 if last else 1), total_steps=scenario.total_steps, current_step_order=1)
    return redirect("trainer:practice", progress_id=progress.pk)


@login_required
def retry_scenario(request, pk):
    scenario = get_object_or_404(Scenario, pk=pk, is_active=True)
    UserProgress.objects.filter(user=request.user, scenario=scenario, status="in_progress").delete()
    return redirect("trainer:start_scenario", pk=scenario.pk)


def _normalize(text):
    return (text or "").strip().replace(" ", "").replace("　", "").lower()


@login_required
def practice(request, progress_id):
    progress = get_object_or_404(UserProgress.objects.select_related("scenario"), pk=progress_id, user=request.user)
    scenario = progress.scenario
    if progress.status == "completed":
        return redirect("trainer:result", progress_id=progress.pk)
    step = ConversationStep.objects.filter(scenario=scenario, order=progress.current_step_order).prefetch_related("choices").first()
    if step is None:
        progress.status, progress.completed_at = "completed", timezone.now()
        progress.save(update_fields=["status", "completed_at"])
        progress.recalculate_score()
        return redirect("trainer:result", progress_id=progress.pk)

    if request.method == "POST":
        is_correct, given_text = False, ""
        if step.answer_type == "choice":
            choice = AnswerChoice.objects.filter(pk=request.POST.get("choice"), step=step).first()
            if choice:
                given_text, is_correct = choice.text, choice.is_correct
        else:
            given_text = request.POST.get("answer_text", "")
            is_correct = _normalize(given_text) == _normalize(step.correct_answer_text)
        UserStepAnswer.objects.create(progress=progress, step=step, given_answer_text=given_text, is_correct=is_correct)
        if is_correct:
            progress.correct_answers += 1
            messages.success(request, "正解です！ Ajoyib — to'g'ri javob.")
        else:
            messages.error(request, "もう一度！ Bu safar xato. Keyingi qadamda yaxshiroq urinib ko'ring.")
        progress.current_step_order += 1
        progress.save(update_fields=["correct_answers", "current_step_order"])
        return redirect("trainer:practice", progress_id=progress.pk)

    total = scenario.total_steps
    answered = progress.current_step_order - 1
    return render(request, "trainer/practice.html", {
        "progress": progress, "scenario": scenario, "step": step,
        "step_number": progress.current_step_order, "total_steps": total,
        "percent": int(answered / total * 100) if total else 0,
        "choices": step.choices.all(),
    })


@login_required
def result(request, progress_id):
    progress = get_object_or_404(UserProgress, pk=progress_id, user=request.user)
    answers = progress.answers.select_related("step").order_by("step__order")
    return render(request, "trainer/result.html", {"progress": progress, "answers": answers})


@login_required
def history(request):
    records = UserProgress.objects.filter(user=request.user).select_related("scenario").order_by("-started_at")
    completed = records.filter(status="completed")
    stats = {
        "total_attempts": records.count(), "completed_count": completed.count(),
        "avg_score": round(completed.aggregate(v=Avg("score"))["v"] or 0, 1),
        "best_score": round(completed.order_by("-score").first().score, 1) if completed.exists() else 0,
    }
    return render(request, "trainer/history.html", {"records": records, **stats})

# Nihongo Talk Trainer — Enhanced Multilingual Edition

Django web app for Japanese conversation practice with learning history, review/retry, voice features, and teacher/admin scenario management.

## Fixed

The project now targets **Django 5.2.17** instead of Django 5.0.7. This is important for Python 3.14: Django 5.0 officially supports only Python 3.10–3.12, while Django 5.2.8+ supports Python 3.14. The 5.2 LTS line is used here.

## Languages

The interface can be switched instantly between:

- 🇺🇿 Uzbek
- 🇯🇵 Japanese
- 🇬🇧 English

The selection is saved in browser localStorage.

## Voice

- Japanese text-to-speech via browser Speech Synthesis API.
- Japanese speech-to-text answer input when the browser supports SpeechRecognition.

## Japan flag animation

The login and start buttons have a small animated Japanese flag above them. The login/register cards also receive the same visual treatment.

## Install / run on Windows

Use the same Python installation that you use for the project.

```powershell
cd C:\Users\User\OneDrive\Рабочий стол\nihongo_trainer_upgraded
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

If you already have Django 5.0.7 installed, the `pip install -r requirements.txt` command is important: it upgrades Django to 5.2.17 and resolves the Python 3.14 incompatibility behind the admin `Context.__copy__` error.

## Admin

Open `/admin/` and log in with your existing superuser. Do not use a demo password in production.

## Main required features

1. Practice Dialogue
2. Learning History
3. Review / Retry
4. Admin Scenario Management

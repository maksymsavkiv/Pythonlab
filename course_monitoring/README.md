# ЛР15 — Course Monitoring

Варіант 18: Кімната 3D друку.

План даних: Принтер стіл (V18-A), Принтер шафа (V18-B), Офіс (V18-C). Два паспорти: Стіл друку, Шафа матеріалу. Мітки: Друк, Полімер, Резерв. Планується 10 вимірювань UTC, пошук «Принтер», поріг 42 °C. Позначати лише температуру > 42, рівність не є перевищенням. Моделі та маршрути monitoring ще не реалізовано.

## Запуск Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -VV
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m django --version
.\.venv\Scripts\python.exe -c "import sqlite3, ctypes; print(sqlite3.sqlite_version)"
.\.venv\Scripts\python.exe -m pip freeze | Out-File -Encoding ascii requirements-lock.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Можна обрати Python 3.13 або 3.14 замість 3.12. Фактичний повний номер вписати після запуску. Django 6.1.2 задано методичкою. requirements-reference.txt — список зі зразка, не результат власного pip freeze. На Windows за потреби встановити tzdata в середовище, після чого повторити freeze.

Перевірити http://127.0.0.1:8000/ (200) та /missing/ (404) у Network. Зупинити Ctrl+C.

```powershell
.\.venv\Scripts\python.exe manage.py shell
```

```python
from django.http import HttpResponse
response = HttpResponse("Навчальний приклад")
print(response.status_code)
print(response.content.decode())
exit()
```

```powershell
.\.venv\Scripts\python.exe -m flask --app framework_examples.flask_app run --host 127.0.0.1 --port 5000
```

Перевірити / та /devices/1 на http://127.0.0.1:5000. Зупинити Ctrl+C.

Git: git init; git add .; git status; git diff --cached; git commit -m "Lab 15". Створити погоджений репозиторій GitHub, додати remote і виконати push. Клонувати в іншу порожню папку, створити нове .venv тієї ж версії Python, встановити requirements-lock.txt, повторити migrate, check і HTTP-перевірку.

Фактичні результати, версії та GitHub-посилання заповнюються після локального запуску. Секретний ключ у settings.py — лише публічна навчальна заглушка, не для розгортання.

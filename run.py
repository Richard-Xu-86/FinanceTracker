import os
import django
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FinanceTracker.settings")
django.setup()

try:
    call_command("migrate", interactive=False)
    call_command("collectstatic", "--noinput")
except Exception as e:
    print("Setup failed:", e)

# Start the app using gunicorn
os.system("gunicorn FinanceTracker.wsgi:application")

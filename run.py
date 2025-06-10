import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FinanceTracker.settings")
django.setup()

from django.core.management import call_command

# Only run migrations the first time
try:
    call_command('migrate', interactive=False)
except Exception as e:
    print("Migration failed:", e)

# Now run the actual server
os.system("gunicorn FinanceTracker.wsgi:application")

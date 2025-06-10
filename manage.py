# The main control script

#modules let us interact with our computer system
import os #lets you work with environment variables
import sys #lets you access command arguments such as runserver and migrate

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main(): # this is like pressing the start button for all django commands
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinanceTracker.settings') #tells django the settings you should use are in FinanceTracker
    try:
        from django.core.management import execute_from_command_line #built in command runer
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

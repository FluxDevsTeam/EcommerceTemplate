import os
from celery import Celery
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get DJANGO_ENV from .env file (defaults to 'dev' if not set)
django_env = os.getenv("DJANGO_ENV", "development").lower()

# Map DJANGO_ENV to the corresponding settings module
settings_module = f"config.settings.{django_env}"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
# Create Celery app instance
app = Celery('KidsDesignCompany')  # Keep your project name

# Load Celery config from Django settings with 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in apps (e.g., payment/tasks.py)
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
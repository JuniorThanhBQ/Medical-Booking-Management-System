from src import create_app
from src.extensions import celery_app

app = create_app()
app.app_context().push()

from loguru import logger
from app.application.tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def generate_content_task(self, content_id: int):
    try:
        logger.info(f"Generating content: {content_id}")
        return {"status": "success", "content_id": content_id}
    except Exception as e:
        logger.error(f"Failed to generate content: {e}")
        self.retry(exc=e, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def polish_content_task(self, content_id: int):
    try:
        logger.info(f"Polishing content: {content_id}")
        return {"status": "success", "content_id": content_id}
    except Exception as e:
        logger.error(f"Failed to polish content: {e}")
        self.retry(exc=e, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def detect_ai_task(self, content_id: int):
    try:
        logger.info(f"Detecting AI content: {content_id}")
        return {"status": "success", "content_id": content_id}
    except Exception as e:
        logger.error(f"Failed to detect AI content: {e}")
        self.retry(exc=e, countdown=5)

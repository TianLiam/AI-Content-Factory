from loguru import logger
from app.application.tasks.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def collect_signals_task(self, platforms: list[str]):
    try:
        logger.info(f"Collecting signals from platforms: {platforms}")
        return {"status": "success", "collected": 0}
    except Exception as e:
        logger.error(f"Failed to collect signals: {e}")
        self.retry(exc=e, countdown=5)


@celery_app.task(bind=True, max_retries=3)
def analyze_signal_task(self, signal_id: int):
    try:
        logger.info(f"Analyzing signal: {signal_id}")
        return {"status": "success", "signal_id": signal_id}
    except Exception as e:
        logger.error(f"Failed to analyze signal: {e}")
        self.retry(exc=e, countdown=5)

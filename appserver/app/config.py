import os
import logging
from functools import lru_cache
from firebase_admin import credentials, initialize_app
from pydantic import BaseSettings


log = logging.getLogger(__name__)


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = bool(os.getenv("TESTING", ""))


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()


def firebase_authenticate():
    storage_bucket = os.environ.get("FIREBASE_STORAGE_BUCKET")
    cred = credentials.Certificate(
        {
            "type": "service_account",
            "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
            "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
            "private_key": os.environ.get("FIREBASE_PRIVATE_KEY").replace("\\n", "\n"),
            "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
            "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": os.environ.get("FIREBASE_CLIENT_CERT_URL"),
        }
    )
    initialize_app(cred, {"storageBucket": storage_bucket})

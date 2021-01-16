import os

import firebase_admin
from app.config import firebase_credentials
from firebase_admin import db, messaging


class Notifier:
    def __init__(self, credentials):
        db_url = os.environ.get("FIREBASE_DB_URL")
        notifications_db_path = os.environ.get("FIREBASE_DB_NOTIFICATIONS_PATH")

        self.app = firebase_admin.initialize_app(
            credentials, {"databaseURL": db_url}, name="bookbnb-notifications"
        )

        self.db_tokens = db.reference(f"/{notifications_db_path}", app=self.app)

    def set_push_token(self, uuid: int, token: str):
        self.db_tokens.update({str(uuid): token})

    def get_push_token(self, uuid: int):
        return self.db_tokens.child(str(uuid)).get()

    def remove_push_token(self, uuid: int):
        removed_token = self.get_push_token(uuid)
        self.db_tokens.child(str(uuid)).delete()
        return removed_token

    def send_notification_test(self, sender: dict, receiver: dict):
        title = "New test notification."
        body = f'Body of test notification from {sender["name"]}'

        self.notify(title, body, receiver["id"])

    def notify(self, title: str, body: str, uuid: int):
        """
        Sends a notification to the users device.
        If the device is not registered to receive notifications,
        no action is performed
        """

        token = self.get_push_token(uuid)
        if not token:
            return False

        _response = self._send_notification(title, body, str(token))
        return True

    def _send_notification(self, title: str, body: str, token: str):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )

        return messaging.send(message, app=self.app)


class NotifierFake:
    def __init__(self, _credentials):
        return

    def set_push_token(self, uuid: int, token: str):
        return

    def get_push_token(self, uuid: int):
        return

    def send_notification_test(self, sender: dict, receiver: dict):
        title = "New test notification."
        body = f'Body of test notification from {sender["name"]}'

        self.notify(title, body, receiver["id"])

    def notify(self, title: str, body: str, uuid: int):
        return

    def _send_notification(self, title: str, body: str, token: str):
        return


notifier = None
if os.environ.get("ENVIRONMENT") == "production":
    notifier = Notifier(firebase_credentials)
else:
    notifier = NotifierFake(firebase_credentials)

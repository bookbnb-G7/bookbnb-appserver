import os
from datetime import datetime

import firebase_admin
from app.config import firebase_credentials
from firebase_admin import db


class ChatFirebase:
    def __init__(self, credentials):
        db_url = os.environ.get("FIREBASE_DB_URL")

        chat_db_path = os.environ.get("FIREBASE_DB_CHAT_PATH")
        message_db_path = os.environ.get("FIREBASE_DB_MESSAGE_PATH")

        self.app = firebase_admin.initialize_app(
            credentials, {"databaseURL": db_url}, name="bookbnb-chat"
        )

        self.db_chats = db.reference(f"/{chat_db_path}", app=self.app)
        self.db_messages = db.reference(f"/{message_db_path}", app=self.app)

    def send_message(self, message, sender: dict, receiver: dict):
        chat_name = self._create_chat_name(sender["uuid"], receiver["uuid"])

        message_data = {
            "sender_name": sender["name"],
            "receiver_name": receiver["name"],
            "sender_uuid": sender["uuid"],
            "receiver_uuid": receiver["uuid"],
            "message": message,
            "timestamp": int(datetime.now().timestamp()),
        }

        chat_db_data = {
            "timestamp": message_data["timestamp"],
            "last_message": message_data,
        }

        self.db_messages.child(chat_name).push(message_data)
        self.db_chats.child("-" + str(sender["uuid"])).child("-" + str(receiver["uuid"])).set(
            chat_db_data
        )
        self.db_chats.child("-" + str(receiver["uuid"])).child("-" + str(sender["uuid"])).set(
            chat_db_data
        )

        return message_data

    def get_messages_between(self, user_a_uuid: int, user_b_uuid: int):
        chat_name = self._create_chat_name(user_a_uuid, user_b_uuid)

        chat = self.db_messages.child(chat_name).get()

        if (chat is None):
            return []

        messages = []
        for timestamp, message in chat.items():
            messages.append(message)

        return messages

    def get_all_chats_from(self, user_uuid: int):
        chats = self.db_chats.child("-" + str(user_uuid)).get()

        if (chats is None):
            return []

        previews = []
        for uuid, chat in chats.items():
            if chat is None:
                continue

            last_message = chat["last_message"]

            if user_uuid == last_message["sender_uuid"]:
                other_user = last_message["receiver_name"]
                other_uuid = last_message["receiver_uuid"]
            else:
                other_user = last_message["sender_name"]
                other_uuid = last_message["sender_uuid"]

            preview = {
                "other_user": other_user,
                "other_uuid": other_uuid,
                "last_message": last_message["message"],
            }

            previews.append(preview)

        return previews

    @staticmethod
    def _create_chat_name(sender_uuid, receiver_uuid):
        if sender_uuid > receiver_uuid:
            chat_name = f"{sender_uuid}-{receiver_uuid}"
        else:
            chat_name = f"{receiver_uuid}-{sender_uuid}"

        return chat_name


class ChatFake:
    def __init__(self, _credentials):
        return

    def send_message(self, message, sender, receiver):
        return

    def get_messages_between(self, user_a, user_b):
        return

    def get_all_chats_from(self, user):
        return


chat_service = None
if os.environ.get("ENVIRONMENT") == "production":
    chat_service = ChatFirebase(firebase_credentials)
else:
    chat_service = ChatFake(firebase_credentials)

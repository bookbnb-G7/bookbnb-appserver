import os
import datetime
import firebase_admin
from firebase_admin import db


class ChatFirebase:
    def __init__(self, credentials):
        db_url = os.environ.get('FIREBASE_DB_URL')

        chat_db_path = os.environ.get('FIREBASE_DB_CHAT_PATH')
        message_db_path = os.environ.get('FIREBASE_DB_MESSAGE_PATH')

        self.app = firebase_admin.initialize_app(
            credentials, {'databaseURL': db_url}, name='bookbnb-chat'
        )

        self.db_chat = db.reference(f'/{chat_db_path}', app=self.app)
        self.db_message = db.reference(f'/{message_db_path}', app=self.app)

    def send_message(self, message, sender, receiver):
        chat_name = self._create_chat_name(sender["uuid"], receiver["uuid"])

        message_data = {
            'sender_name': sender["name"],
            'receiver_name': receiver["name"],

            'sender_uuid': sender["uuid"],
            'receiver_uuid': receiver["uuid"],

            'message': message,
            'timestamp': int(datetime.datetime.now().timestamp())
        }

        chat_db_data = {
            'timestamp': message_data['timestamp'],
            'last_message': message_data['message']
        }

        self.db_message.child(chat_name).push(message_data)
        self.db_chat.child(str(sender['uuid'])).child(str(receiver['uuid'])).set(chat_db_data)
        self.db_chat.child(str(receiver['uuid'])).child(str(sender['uuid'])).set(chat_db_data)

    @staticmethod
    def _create_chat_name(sender_uuid, receiver_uuid):
        if sender_uuid > receiver_uuid:
            chat_name = f'{sender_uuid}-{receiver_uuid}'
        else:
            chat_name = f'{receiver_uuid}-{sender_uuid}'

        return chat_name

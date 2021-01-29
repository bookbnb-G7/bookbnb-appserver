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

    # send notification chat new message
    def send_new_chat_message_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        title = "Nuevo mensaje en el chat"
        body = f'Mensaje nuevo de {sender_name}'

        self.notify(title, body, receiver_uuid)

    # send notification new booking received for user's room
    def send_new_booking_received_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Nueva reserva recibida"
        body = f'El usuario {sender_name} hizo una reserva en la habitacion {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification booking made accepted
    def send_booking_accepted_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Se confirmo una reserva realizada"
        body = f'El usuario {sender_name} confirmo la reserva realizada en {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification booking made rejected
    def send_booking_rejected_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Se rechazo una reserva realizada"
        body = f'El usuario {sender_name} rechazo la reserva realizada en {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification new comment for user's room
    def send_new_comment_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Se recibio un nuevo comentario"
        body = f'El usuario {sender_name} comento tu habitacion {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification comment answered
    def send_answered_comment_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Se respondio tu nuevo comentario"
        body = f'El usuario {sender_name} respondio a tu comentario de {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification new rating for user's room
    def send_new_room_rating_notification(
        self, sender_name: str, room_title: str, rating: int, receiver_uuid: int
    ):
        title = "Nueva calificacion en tu habitacion"
        body = f'El usuario {sender_name} califico tu habitacion {room_title} con {rating}'

        self.notify(title, body, receiver_uuid)

    # send notification new review for user's room
    def send_new_room_review_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        title = "Nueva reseña en tu habitacion"
        body = f'El usuario {sender_name} escribio una reseña de tu habitacion {room_title}'

        self.notify(title, body, receiver_uuid)

    # send notification new guest rating for user
    def send_new_user_guest_rating_notification(
        self, sender_name: str, rating: int, receiver_uuid: int
    ):
        title = "Nueva calificacion recibida"
        body = f'El usuario {sender_name} te califico como huesped con {rating}'

        self.notify(title, body, receiver_uuid)

    # send notification new host rating for user
    def send_new_user_host_rating_notification(
        self, sender_name: str, rating: int, receiver_uuid: int
    ):
        title = "Nueva calificacion recibida"
        body = f'El usuario {sender_name} te califico como anfitrion con {rating}'

        self.notify(title, body, receiver_uuid)

    # send notification new guest review for user
    def send_new_user_guest_review_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        title = "Nueva reseña recibida"
        body = f'El usuario {sender_name} escribio una reseña de huesped de tu usuario'

        self.notify(title, body, receiver_uuid)

    # send notification new host review for user
    def send_new_user_host_review_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        title = "Nueva reseña recibida"
        body = f'El usuario {sender_name} escribio una reseña de anfitrion de tu usuario'

        self.notify(title, body, receiver_uuid)

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

    def send_new_chat_message_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        return

    def send_new_booking_received_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_booking_accepted_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_booking_rejected_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_new_comment_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_answered_comment_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_new_room_rating_notification(
        self, sender_name: str, room_title: str, rating: int,
        receiver_uuid: int
    ):
        return

    def send_new_room_review_notification(
        self, sender_name: str, room_title: str, receiver_uuid: int
    ):
        return

    def send_new_user_guest_rating_notification(
        self, sender_name: str, rating: int, receiver_uuid: int
    ):
        return

    def send_new_user_host_rating_notification(
        self, sender_name: str, rating: int, receiver_uuid: int
    ):
        return

    def send_new_user_guest_review_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        return

    def send_new_user_host_review_notification(
        self, sender_name: str, receiver_uuid: int
    ):
        return

    def notify(self, title: str, body: str, uuid: int):
        return

    def _send_notification(self, title: str, body: str, token: str):
        return


notifier = None
if os.environ.get("ENVIRONMENT") == "production":
    notifier = Notifier(firebase_credentials)
else:
    notifier = NotifierFake(firebase_credentials)

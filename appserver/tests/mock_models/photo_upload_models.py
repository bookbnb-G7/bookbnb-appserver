from tests.utils import MockResponse


class MockFirebaseBlob:
    def __init__(self):
        self.public_url = "www.google.com"

    def upload_from_file(self, file):
        pass

    def make_public(self):
        pass

    def delete(self):
        pass


class MockFirebaseBucketResponse:
    def blob(self, name):
        return MockFirebaseBlob()

    def get_blob(self, blob_name):
        return MockFirebaseBlob()


class MockRoomPhotoUploadResponse(MockResponse):
    def dict(self):
        return {
            "url": "urlpiola",
            "firebase_id": 0,
            "id": 0,
            "room_id": 8,
            "created_at": "2020-12-01T19:00:00.033000+00:00",
            "updated_at": "2020-12-01T19:00:00.033000+00:00",
        }


class MockRoomPhotoList(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 8,
            "room_photos": [
                {
                    "url": "urlpiola",
                    "firebase_id": 0,
                    "id": 0,
                    "room_id": 8,
                    "created_at": "2020-12-01T19:00:00.033000+00:00",
                    "updated_at": "2020-12-01T19:00:00.033000+00:00",
                },
                {
                    "url": "otraurl",
                    "firebase_id": 1,
                    "id": 1,
                    "room_id": 8,
                    "created_at": "2020-12-02T19:00:00.033000+00:00",
                    "updated_at": "2020-12-02T19:00:00.033000+00:00",
                },
            ],
        }

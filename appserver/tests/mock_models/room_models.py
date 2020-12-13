from tests.utils import MockResponse


class MockRoomResponse(MockResponse):
    def dict(self):
        return {
            "type": "Apartment",
            "owner": "Carlito",
            "owner_uuid": 10,
            "price_per_day": 999,
            "id": 0,
            "created_at": "2020-11-10T22:51:03.539Z",
            "updated_at": "2020-11-10T22:51:03.539Z",
        }


class MockRoomListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "rooms": [
                {
                    "type": "Apartment",
                    "owner": "Carlito",
                    "owner_uuid": 10,
                    "price_per_day": 999,
                    "id": 0,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "type": "House",
                    "owner": "Freee",
                    "owner_uuid": 11,
                    "price_per_day": 123,
                    "id": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }

from tests.utils import MockResponse


class MockRoomResponse(MockResponse):
    def dict(self):
        return {
            "title": "Exclusive offer in Las Toninas",
            "description": "Apartment with sights to the almighty beach",
            "type": "Apartment",
            "owner": "Carlito",
            "owner_uuid": 10,
            "price_per_day": 999,
            "latitude": 0.0,
            "longitude": 0.0,
            "location": "USA",
            "capacity": 1,
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
                    "id": 0,
                    "title": "Exclusive offer in Las Toninas",
                    "description": "Apartment with sights to the almighty beach",
                    "type": "Apartment",
                    "owner": "Carlito",
                    "owner_uuid": 10,
                    "price_per_day": 999,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "location": "USA",
                    "capacity": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
                {
                    "id": 1,
                    "title": "House offer in Las Toninas",
                    "description": "Masion-like House available for 1",
                    "type": "House",
                    "owner": "Freee",
                    "owner_uuid": 11,
                    "price_per_day": 123,
                    "latitude": 0.0,
                    "longitude": 0.0,
                    "location": "USA",
                    "capacity": 1,
                    "created_at": "2020-11-10T22:51:03.539Z",
                    "updated_at": "2020-11-10T22:51:03.539Z",
                },
            ],
        }


class MockPaymentRoomResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "price": 5,
            "ownerId": 3
        }

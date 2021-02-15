from tests.utils import MockResponse


class MockUserResponse(MockResponse):
    def dict(self):
        return {
            "firstname": "carlito",
            "lastname": "carlos",
            "email": "carlos@aaaaaaa",
            "phonenumber": "08004444",
            "country": "CR",
            "birthdate": "9999-99-99",
            "photo": "https://bit.ly/3prghP8",
            "id": 12,
            "createdAt": "2020-11-10T22:51:03.539Z",
            "updatedAt": "2020-11-10T22:51:03.539Z",
        }


class MockUserListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "users": [
                {
                    "firstname": "carlito",
                    "lastname": "carlos",
                    "email": "carlos@aaaaaaa",
                    "phonenumber": "08004444",
                    "country": "CR",
                    "birthdate": "9999-99-99",
                    "photo": "otrolinkkkk",
                    "id": 8,
                    "createdAt": "2020-11-10T22:51:03.539Z",
                    "updatedAt": "2020-11-10T22:51:03.539Z",
                },
                {
                    "firstname": "elmer",
                    "lastname": "figueroa",
                    "email": "carlos@eeee",
                    "phonenumber": "08004444",
                    "country": "CHY",
                    "birthdate": "9999-99-99",
                    "photo": "unlinkkkkk",
                    "id": 45,
                    "createdAt": "2020-11-10T22:51:03.539Z",
                    "updatedAt": "2020-11-10T22:51:03.539Z",
                },
            ],
        }


class MockPaymentWalletResponse(MockResponse):
    def dict(self):
        return {
            "uuid": 4,
            "address": "fake_addr",
            "mnemonic": "word word word word word word word word word word word word",
            "balance": 0.24,
        }


class MockFavoriteRoomResponse(MockResponse):
    def dict(self):
        return {
            "room_id": 5,
            "userId": 27,
            "id": 45,
            "createdAt": "2020-11-10T22:51:03.539Z",
            "updatedAt": "2020-11-10T22:51:03.539Z",
        }


class MockFavoriteRoomListResponse(MockResponse):
    def dict(self):
        return {
            "userId": 27,
            "amount": 2,
            "favorites": [
                {
                    "room_id": 5,
                    "userId": 27,
                    "id": 45,
                    "createdAt": "2020-11-10T22:51:03.539Z",
                    "updatedAt": "2020-11-10T22:51:03.539Z",
                },
                {
                    "room_id": 6,
                    "userId": 27,
                    "id": 46,
                    "createdAt": "2020-11-10T22:51:03.539Z",
                    "updatedAt": "2020-11-10T22:51:03.539Z",
                },
            ]
        }



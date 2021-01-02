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
            "photo": "https://www.cmtv.com.ar/imagenes_artistas/70.jpg?Chayanne",
            "id": 12,
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
                },
            ],
        }

class MockPaymentWalletResponse(MockResponse):
    def dict(self):
        return {
            "uuid": 4,
            "address": "fake_addr",
            "mnemonic": "word word word word word word word word word word word word"
        }

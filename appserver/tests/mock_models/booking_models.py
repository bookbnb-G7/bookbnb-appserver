from tests.utils import MockResponse


class MockBookingResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "price": 5,
            "roomId": 5,
            "bookerId": 5,
            "roomOwnerId": 8,
            "dateFrom": "2020-12-14",
            "dateTo": "2020-12-19",
            "bookingStatus": 0,
            "transactionStatus": 3,
            "transactionHash": "HASHRELOCO"
        }


class MockBookingAcceptedResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "price": 5,
            "roomId": 5,
            "bookerId": 5,
            "roomOwnerId": 8,
            "dateFrom": "2020-12-14",
            "dateTo": "2020-12-19",
            "bookingStatus": 2,
            "transactionStatus": 3,
            "transactionHash": "HASHRELOCO"
        }

class MockBookingRejectedResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "price": 5,
            "roomId": 5,
            "bookerId": 5,
            "roomOwnerId": 8,
            "dateFrom": "2020-12-14",
            "dateTo": "2020-12-19",
            "bookingStatus": 2,
            "transactionStatus": 3,
            "transactionHash": "HASHRELOCO"
        }



class MockBookingListResponse(MockResponse):
    def dict(self):
        return [
            {
                "id": 4,
                "price": 5,
                "roomId": 5,
                "bookerId": 5,
                "roomOwnerId": 8,
                "dateFrom": "2020-12-14",
                "dateTo": "2020-12-19",
                "bookingStatus": 0,
                "transactionStatus": 3,
                "transactionHash": "HASHRELOCO"
            },
            {
                "id": 8,
                "price": 20,
                "roomId": 6,
                "bookerId": 4,
                "roomOwnerId": 9,
                "dateFrom": "2020-10-01",
                "dateTo": "2020-10-04",
                "bookingStatus": 0,
                "transactionStatus": 3,
                "transactionHash": "HASHRELOCO"
            },
        ]


class MockRoomBookingResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "date_from": "2020-12-14",
            "date_to": "2020-12-19"
        }

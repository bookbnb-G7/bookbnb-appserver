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
            "transactionHash": "HASHRELOCO",
            "createdAt": "2020-11-10T22:51:03.539Z",
            "updatedAt": "2020-11-10T22:51:03.539Z",
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
            "transactionHash": "HASHRELOCO",
            "createdAt": "2020-11-10T22:51:03.539Z",
            "updatedAt": "2020-11-10T22:51:03.539Z",
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
            "transactionHash": "HASHRELOCO",
            "createdAt": "2020-11-10T22:51:03.539Z",
            "updatedAt": "2020-11-10T22:51:03.539Z",
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
                "transactionHash": "HASHRELOCO",
                "createdAt": "2020-11-10T22:51:03.539Z",
                "updatedAt": "2020-11-10T22:51:03.539Z",
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
                "transactionHash": "HASHRELOCO",
                "createdAt": "2020-11-10T22:51:03.539Z",
                "updatedAt": "2020-11-10T22:51:03.539Z",
            },
        ]


class MockRoomBookingResponse(MockResponse):
    def dict(self):
        return {"id": 4, "date_from": "2020-12-14", "date_to": "2020-12-19"}

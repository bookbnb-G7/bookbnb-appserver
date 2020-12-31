from tests.utils import MockResponse


class MockBookingResponse(MockResponse):
    def dict(self):
        return {
            "user_id": 4,
            "date_ends": "2020-12-19T01:16:34.275Z",
            "date_begins": "2020-12-14T01:16:34.275Z",
            "amount_of_people": 2,
            "id": 7,
            "room_id": 5,
            "total_price": 876.5,
            "status": 1,
            "created_at": "2020-12-14T01:16:34.275Z",
            "updated_at": "2020-12-14T01:16:34.275Z",
        }


class MockBookingListResponse(MockResponse):
    def dict(self):
        return {
            "amount": 2,
            "room_id": 6,
            "bookings": [
                {
                    "user_id": 4,
                    "date_ends": "2020-12-14T01:16:34.275Z",
                    "date_begins": "2020-12-19T01:16:34.275Z",
                    "amount_of_people": 2,
                    "id": 7,
                    "room_id": 6,
                    "total_price": 876.5,
                    "status": 1,
                    "created_at": "2020-12-14T01:16:34.275Z",
                    "updated_at": "2020-12-14T01:16:34.275Z",
                },
                {
                    "user_id": 4,
                    "date_ends": "2020-10-04T01:16:34.275Z",
                    "date_begins": "2020-10-01T01:16:34.275Z",
                    "amount_of_people": 2,
                    "id": 8,
                    "room_id": 6,
                    "total_price": 466.3,
                    "status": 1,
                    "created_at": "2020-12-14T01:16:34.275Z",
                    "updated_at": "2020-12-14T01:16:34.275Z",
                },
            ],
        }


class MockUserBookingResponse(MockResponse):
    def dict(self):
        return {
            "booking_id": 4,
            "room_id": 5,
        }


class MockUserBookingListResponse(MockResponse):
    def dict(self):
        return {
            "userId": 5,
            "amount": 2,
            "roomBookings": [
                {
                    "booking_id": 4,
                    "room_id": 5,
                },
                {
                    "booking_id": 6,
                    "room_id": 9,
                },
            ],
        }


class MockPaymentBookingResponse(MockResponse):
    def dict(self):
        return {
            "id": 4,
            "price": 5,
            "roomId": 5,
            "bookerId": 5,
            "dateFrom": "2020-12-14",
            "dateTo": "2020-12-19",
            "bookingStatus": 1,
            "transactionStatus": 3,
            "transactionHash": "HASHRELOCO"
        }

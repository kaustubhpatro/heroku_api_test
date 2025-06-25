import pytest
from models.booking import Booking


@pytest.mark.parametrize("payload", [
    {"firstname": "Alice", "lastname": "Tyler", "totalprice": 100, "depositpaid": True,
     "bookingdates": {"checkin": "2025-01-01", "checkout": "2025-01-03"}},
    {"firstname": "Bob", "lastname": "Marley", "totalprice": 200, "depositpaid": False,
     "bookingdates": {"checkin": "2025-02-01", "checkout": "2025-02-04"}},
])
def test_create_booking_success(client, payload):
    resp = client.create(payload)
    assert "bookingid" in resp and isinstance(resp["bookingid"], int)

    booking = Booking.parse_obj(resp["booking"])
    assert booking.firstname == payload["firstname"]
    assert booking.lastname == payload["lastname"]

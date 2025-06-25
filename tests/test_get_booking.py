import pytest
from models.booking import Booking
from datetime import date, timedelta


@pytest.mark.parametrize("days_ahead", [0, 1, 5])
def test_get_booking(client, days_ahead):
    payload = {
        "firstname": "Test", "lastname": "User", "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": date.today().isoformat(),
            "checkout": (date.today() + timedelta(days=days_ahead)).isoformat()
        }
    }
    bid = client.create(payload)["bookingid"]
    resp = client.get(bid)
    booking = Booking.parse_obj(resp)
    assert booking.bookingdates.checkout.endswith(
        (date.today() + timedelta(days=days_ahead)).isoformat()
    )

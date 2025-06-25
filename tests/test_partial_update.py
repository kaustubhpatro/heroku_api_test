import pytest
from faker import Faker
from models.booking import Booking

faker = Faker()


@pytest.mark.parametrize("field", ["firstname", "lastname"])
def test_patch_booking(client, token, booking_payload, field):
    # create
    bid = client.create(booking_payload)["bookingid"]
    new_val = faker.first_name() if field == "firstname" else faker.last_name()
    updated = client.partial_update(bid, {field: new_val}, token)
    assert updated[field] == new_val

    # verify full
    full = Booking.parse_obj(client.get(bid))
    assert getattr(full, field) == new_val

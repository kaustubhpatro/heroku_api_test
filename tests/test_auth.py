import pytest


def test_successful_auth(client, token):
    assert isinstance(token, str) and token


@pytest.mark.parametrize("user,passwd", [
    ("admin", "password123"),
    ("admin", "wrong"),
])
def test_auth_various(client, user, passwd):
    if passwd == "password123":
        tok = client.auth(user, passwd)
        assert isinstance(tok, str)
    else:
        with pytest.raises(Exception):
            client.auth(user, passwd)

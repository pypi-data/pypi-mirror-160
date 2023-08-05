from simplelogin import SimpleLoginApi
from tests import TClient


def test_get_user():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {
        'email': 'user@example.com',
        'in_trial': False,
        'is_premium': True,
        'name': '',
        'profile_picture_url': 'https://example.com/image.png'
    }
    cli.push_response(200, rsp)
    r = api.get_user_info().to_native()
    assert r == rsp

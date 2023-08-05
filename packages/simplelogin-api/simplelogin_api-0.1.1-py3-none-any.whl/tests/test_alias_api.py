from simplelogin import SimpleLoginApi
from tests import TClient
from datetime import datetime, timezone
now = datetime.now(tz=timezone.utc)


def test_get_alias_options():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {'can_create': True,
           'prefix_suggestion': 'prefix',
           'suffixes': [{'signed_suffix': '.2o81f@8alias.com.signature',
                         'suffix': '.2o81f@8alias.com'},
                        {'signed_suffix': '.a3lnp@dralias.com.signature',
                         'suffix': '.a3lnp@dralias.com'},
                        {'signed_suffix': '.j95vv@aleeas.com.signature',
                         'suffix': '.j95vv@aleeas.com'}]
           }
    cli.push_response(200, rsp)
    r = api.get_alias_options(hostname='prefix').to_native()
    assert r == rsp

def test_get_alias_list():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {'aliases': [{'alias': None,
                        'creation_date': now,
                        'creation_timestamp': now,
                        'disable_pgp': False,
                        'email': 'mail1@aleeas.com',
                        'enabled': True,
                        'id': 123,
                        'latest_activity': None,
                        'mailbox': {'email': 'mail@example.com', 'id': 123456},
                        'mailboxes': [{'email': 'mail@example.com', 'id': 123456}],
                        'name': None,
                        'nb_block': 0,
                        'nb_forward': 0,
                        'nb_reply': 0,
                        'note': None,
                        'pinned': False,
                        'support_pgp': False},
                       {'alias': None,
                        'creation_date': now,
                        'creation_timestamp': now,
                        'disable_pgp': False,
                        'email': 'mail2@aleeas.com',
                        'enabled': True,
                        'id': 124,
                        'latest_activity': None,
                        'mailbox': {'email': 'mail@example.com', 'id': 123456},
                        'mailboxes': [{'email': 'mail@example.com', 'id': 123456}],
                        'name': None,
                        'nb_block': 0,
                        'nb_forward': 0,
                        'nb_reply': 0,
                        'note': None,
                        'pinned': False,
                        'support_pgp': False}]}

    cli.push_response(200, rsp)
    r = api.get_alias_list(page=0).to_native()
    assert r == rsp

def test_create_random_alias():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {'alias': '2a2f6072-5c7c-43de-894e-9b993bcb90d3@aleeas.com',
           'creation_date': now,
           'creation_timestamp': now,
           'disable_pgp': False,
           'email': '2a2f6072-5c7c-43de-894e-9b993bcb90d3@aleeas.com',
           'enabled': True,
           'id': 123,
           'latest_activity': None,
           'mailbox': {'email': 'mail@example.com', 'id': 123456},
           'mailboxes': [{'email': 'mail@example.com', 'id': 123456}],
           'name': None,
           'nb_block': 0,
           'nb_forward': 0,
           'nb_reply': 0,
           'note': 'yay note',
           'pinned': False,
           'support_pgp': False}
    cli.push_response(201, rsp)
    r = api.create_random_alias(mode='uuid', note='yay note').to_native()
    assert r == rsp

def test_get_alias():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {'alias': None,
           'creation_date': now,
           'creation_timestamp': now,
           'disable_pgp': False,
           'email': '2a2f6072-5c7c-43de-894e-9b993bcb90d3@aleeas.com',
           'enabled': True,
           'id': 123,
           'latest_activity': None,
           'mailbox': {'email': 'mail@example.com', 'id': 123456},
           'mailboxes': [{'email': 'mail@example.com', 'id': 123456}],
           'name': None,
           'nb_block': 0,
           'nb_forward': 0,
           'nb_reply': 0,
           'note': 'yay note',
           'pinned': False,
           'support_pgp': False}
    cli.push_response(200, rsp)
    r = api.get_alias(123).to_native()
    assert r == rsp

def test_delete_alias():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {
        'deleted': True
    }
    cli.push_response(200, rsp)
    r = api.delete_alias(123).to_native()
    assert r == rsp

def test_toggle_alias():
    cli = TClient()
    api = SimpleLoginApi(cli)
    rsp = {
        'enabled': True
    }
    cli.push_response(200, rsp)
    r = api.toggle_alias(123).to_native()
    assert r == rsp

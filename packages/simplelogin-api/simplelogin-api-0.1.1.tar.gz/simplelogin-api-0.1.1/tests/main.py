import logging
from pprint import pprint
from schematics import types
from simplelogin.client import Client
from simplelogin import SimpleLoginApi
from simplelogin.definitions import Endpoint

API_KEY = 'tbuciuzwtovorvpkfwzteilpspzrajidtmdcquiwtacypnmxuuoitwxswtsp'


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    client = Client(API_KEY)
    api = SimpleLoginApi(client)
    pprint(api.get_user_info().to_native())
    # pprint(api.get_mailbox_list().to_native())
    # for page in range(100):
    #     l = api.get_alias_list(page=page)
    #     if len(l.aliases) == 0:
    #         break
    #     for e in l.aliases:  # type: ddefs.AliasInfo
    #         api.delete_alias(e.id)

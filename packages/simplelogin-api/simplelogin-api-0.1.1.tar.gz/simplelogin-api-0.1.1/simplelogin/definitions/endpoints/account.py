from schematics import types

import simplelogin.definitions.data.account
from simplelogin.definitions import Endpoint, data as ddefs

# ================================================================
class GetUser(Endpoint):
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/user_info')
    status_code = types.ListType(types.IntType(), default=(200,))
    rsp_type = simplelogin.definitions.data.account.UserInfo

from schematics import types
from simplelogin.definitions import EndpointParams, Endpoint
from simplelogin.definitions.data import mailbox as ddefs

# ================================================================
class GetMailboxList(Endpoint):
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/v2/mailboxes')
    status_code = types.ListType(types.IntType(), default=(200,))
    rsp_type = ddefs.MailboxList

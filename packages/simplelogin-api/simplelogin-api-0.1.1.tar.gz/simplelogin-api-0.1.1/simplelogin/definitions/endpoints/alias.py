from schematics import types
from simplelogin.definitions import EndpointParams, Endpoint
from simplelogin.definitions.data import alias as ddefs

# ================================================================
class GetAliasOptionsQuery(EndpointParams):
    hostname = types.StringType()

class GetAliasOptions(Endpoint):
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/v5/alias/options')
    status_code = types.ListType(types.IntType(), default=(200,))
    query_type = GetAliasOptionsQuery
    rsp_type = ddefs.AliasOptions

# ================================================================
class GetAliasListQuery(EndpointParams):
    page_id = types.IntType(default=0)
    pinned = types.BooleanType()

class GetAliasList(Endpoint):
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/v2/aliases')
    status_code = types.ListType(types.IntType(), default=(200,))
    query_type = GetAliasListQuery
    rsp_type = ddefs.AliasInfoList

# ================================================================
class CreateRandomAliasQuery(EndpointParams):
    hostname = types.StringType()
    mode = types.StringType(choices=['uuid', 'word'])

class CreateRandomAliasData(EndpointParams):
    note = types.StringType()

class CreateRandomAlias(Endpoint):
    method = types.StringType(default='POST')
    url = types.StringType(default='/api/alias/random/new')
    status_code = types.ListType(types.IntType(), default=(201,))
    query_type = CreateRandomAliasQuery
    data_type = CreateRandomAliasData
    rsp_type = ddefs.AliasInfo

# ================================================================
class CreateCustomAliasQuery(EndpointParams):
    hostname = types.StringType()

class CreateCustomAliasData(EndpointParams):
    alias_prefix = types.StringType(required=True)
    signed_suffix = types.StringType(required=True)
    mailbox_ids = types.ListType(types.IntType(), required=True)
    note = types.StringType()
    name = types.StringType()

class CreateCustomAlias(Endpoint):
    method = types.StringType(default='POST')
    url = types.StringType(default='/api/v3/alias/custom/new')
    status_code = types.ListType(types.IntType(), default=(201,))
    query_type = CreateCustomAliasQuery
    data_type = CreateCustomAliasData
    rsp_type = ddefs.AliasInfo

# ================================================================
class GetAlias(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/aliases/{}')
    status_code = types.ListType(types.IntType(), default=(200,))
    rsp_type = ddefs.AliasInfo

# ================================================================
class UpdateAliasData(EndpointParams):
    note = types.StringType()
    mailbox_id = types.IntType()
    name = types.StringType()
    mailbox_ids = types.ListType(types.IntType())
    disable_pgp = types.BooleanType()
    pinned = types.BooleanType()

class UpdateAlias(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='PATCH')
    url = types.StringType(default='/api/aliases/{}')
    status_code = types.ListType(types.IntType(), default=(200,))
    data_type = UpdateAliasData

# ================================================================
class ToggleAlias(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='POST')
    url = types.StringType(default='/api/aliases/{}/toggle')
    status_code = types.ListType(types.IntType(), default=(200,))
    rsp_type = ddefs.ToggleAlias

# ================================================================
class DeleteAlias(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='DELETE')
    url = types.StringType(default='/api/aliases/{}')
    status_code = types.ListType(types.IntType(), default=(200,))
    rsp_type = ddefs.DeleteAlias

# ================================================================
class GetAliasActivityListQuery(EndpointParams):
    page_id = types.IntType(default=0)

class GetAliasActivityList(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/aliases/{}/activities')
    status_code = types.ListType(types.IntType(), default=(200,))
    query_type = GetAliasActivityListQuery
    rsp_type = ddefs.AliasActivityList

# ================================================================
class GetAliasContactListQuery(EndpointParams):
    page_id = types.IntType(default=0)

class GetAliasContactList(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='GET')
    url = types.StringType(default='/api/aliases/{}/contacts')
    status_code = types.ListType(types.IntType(), default=(200,))
    query_type = GetAliasContactListQuery
    rsp_type = ddefs.AliasContactList

# ================================================================
class CreateAliasContactData(EndpointParams):
    contact = types.StringType(required=True)

class CreateAliasContact(Endpoint):
    def __post_init__(self, *args, **kwargs):
        self.url = self.url.format(self.alias_id)
    alias_id = types.IntType(required=True)
    method = types.StringType(default='POST')
    url = types.StringType(default='/api/aliases/{}/contacts')
    status_code = types.ListType(types.IntType(), default=(200, 201))
    data_type = CreateAliasContactData
    rsp_type = ddefs.AliasContact

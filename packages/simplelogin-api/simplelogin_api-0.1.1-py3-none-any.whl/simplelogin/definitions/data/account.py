from schematics import types
from simplelogin.definitions import Model

# ================================================================
class UserInfo(Model):
    name = types.StringType()
    is_premium = types.BooleanType()
    email = types.EmailType()
    in_trial = types.BooleanType()
    profile_picture_url = types.URLType()
    max_alias_free_plan = types.IntType()

from schematics import types
from simplelogin.definitions import Model


class AliasOptionsSuffix(Model):
    signed_suffix = types.StringType()
    suffix = types.StringType()

class AliasOptions(Model):
    can_create = types.BooleanType()
    prefix_suggestion = types.StringType()
    suffixes = types.ListType(types.ModelType(AliasOptionsSuffix))

class AliasInfoMailbox(Model):
    id = types.IntType()
    email = types.EmailType()

class AliasInfoContact(Model):
    email = types.EmailType()
    name = types.StringType()
    reverse_alias = types.StringType()

class AliasInfoLatestActivity(Model):
    action = types.StringType()
    contact = types.ModelType(AliasInfoContact)
    timestamp = types.TimestampType()

class AliasInfo(Model):
    creation_date = types.DateTimeType()
    creation_timestamp = types.TimestampType()
    email = types.EmailType()
    alias = types.EmailType()  # copy of email when creating alias
    name = types.StringType()
    enabled = types.BooleanType()
    id = types.IntType()
    support_pgp = types.BooleanType()
    disable_pgp = types.BooleanType()
    mailbox = types.ModelType(AliasInfoMailbox)  # obsolete
    mailboxes = types.ListType(types.ModelType(AliasInfoMailbox))
    latest_activity = types.ModelType(AliasInfoLatestActivity)
    nb_block = types.IntType()
    nb_forward = types.IntType()
    nb_reply = types.IntType()
    note = types.StringType()
    pinned = types.BooleanType()

class AliasInfoList(Model):
    aliases = types.ListType(types.ModelType(AliasInfo))

class DeleteAlias(Model):
    deleted = types.BooleanType()

class ToggleAlias(Model):
    enabled = types.BooleanType()

class AliasActivity(Model):
    action = types.StringType()
    from_ = types.StringType(serialized_name='from')
    timestamp = types.TimestampType()
    to = types.StringType()
    reverse_alias = types.StringType()
    reverse_alias_address = types.EmailType()

class AliasActivityList(Model):
    activities = types.ListType(types.ModelType(AliasActivity))

class AliasContact(Model):
    id = types.IntType()
    contact = types.StringType()
    creation_date = types.DateTimeType()
    creation_timestamp = types.TimestampType()
    last_email_sent_date = types.DateTimeType()
    last_email_sent_timestamp = types.TimestampType()
    existed = types.BooleanType()
    reverse_alias = types.StringType()
    reverse_alias_address = types.EmailType()
    block_forward = types.BooleanType()

class AliasContactList(Model):
    contacts = types.ListType(types.ModelType(AliasContact))

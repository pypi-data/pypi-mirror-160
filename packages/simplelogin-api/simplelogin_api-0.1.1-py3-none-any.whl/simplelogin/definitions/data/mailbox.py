from schematics import types
from simplelogin.definitions import Model

class Mailbox(Model):
    id = types.IntType()
    email = types.EmailType()
    default = types.BooleanType()
    creation_timestamp = types.TimestampType()
    nb_alias = types.IntType()
    verified = types.BooleanType()

class MailboxList(Model):
    mailboxes = types.ListType(types.ModelType(Mailbox))

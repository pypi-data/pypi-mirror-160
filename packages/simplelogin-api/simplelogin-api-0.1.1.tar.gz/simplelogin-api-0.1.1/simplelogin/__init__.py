from simplelogin.client import BaseClient
from simplelogin import exceptions as exc
from simplelogin.definitions.data import \
    account as d_account, \
    alias as d_alias, \
    mailbox as d_mailbox
from simplelogin.definitions.endpoints import \
    account as ep_account, \
    alias as ep_alias, \
    mailbox as ep_mailbox


class SimpleLoginApi:
    def __init__(self, client: BaseClient, base_url: str = 'https://app.simplelogin.io'):
        self._client = client
        self._base_url = base_url

    def get_user_info(self) -> d_account.UserInfo:
        return self._client.make_request(self._base_url, ep_account.GetUser())

    def get_alias_options(self, hostname: str = None) -> d_alias.AliasOptions:
        params = {
            'hostname': hostname,
        }
        return self._client.make_request(self._base_url, ep_alias.GetAliasOptions(), params=params)

    def get_alias_list(self, page: int, pinned: bool = False) -> d_alias.AliasInfoList:
        params = {
            'page_id': page,
        }
        if pinned:
            params['pinned'] = True
        return self._client.make_request(self._base_url, ep_alias.GetAliasList(), params=params)

    def create_random_alias(self, hostname: str = None, mode: str = None, note: str = None) -> d_alias.AliasInfo:
        """
        :param mode: either 'uuid' or 'word'
        """
        params = {
            'hostname': hostname,
            'mode': mode,
        }
        data = {
            'note': note,
        }
        return self._client.make_request(self._base_url, ep_alias.CreateRandomAlias(), params=params, data=data)

    def create_custom_alias(self,
                            alias_prefix: str,
                            signed_suffix: str,
                            mailbox_ids: list[int],
                            hostname: str = None,
                            name: str = None,
                            note: str = None) -> d_alias.AliasInfo:
        params = {
            'hostname': hostname,
        }
        data = {
            'alias_prefix': alias_prefix,
            'signed_suffix': signed_suffix,
            'mailbox_ids': mailbox_ids,
            'note': note,
            'name': name,
        }
        return self._client.make_request(self._base_url, ep_alias.CreateCustomAlias(), params=params, data=data)

    def update_alias(self,
                     alias_id: int,
                     note: str = None,
                     name: str = None,
                     mailbox_ids: list[int] = None,
                     disable_pgp: bool = None,
                     pinned: bool = None,
                     ):
        data = {
            'note': note,
            'name': name,
            'mailbox_ids': mailbox_ids,
            'disable_pgp': disable_pgp,
            'pinned': pinned,
        }
        return self._client.make_request(self._base_url, ep_alias.UpdateAlias({'alias_id': alias_id}), data=data)

    def get_alias(self, alias_id: int) -> d_alias.AliasInfo:
        return self._client.make_request(self._base_url, ep_alias.GetAlias({'alias_id': alias_id}))

    def delete_alias(self, alias_id: int) -> d_alias.DeleteAlias:
        return self._client.make_request(self._base_url, ep_alias.DeleteAlias({'alias_id': alias_id}))

    def toggle_alias(self, alias_id: int) -> d_alias.ToggleAlias:
        return self._client.make_request(self._base_url, ep_alias.ToggleAlias({'alias_id': alias_id}))

    def get_alias_activity_list(self, alias_id: int, page: int) -> d_alias.AliasActivityList:
        params = {
            'page_id': page,
        }
        return self._client.make_request(
            self._base_url,
            ep_alias.GetAliasActivityList({'alias_id': alias_id}),
            params=params
        )

    def get_alias_contact_list(self, alias_id: int, page: int) -> d_alias.AliasContactList:
        params = {
            'page_id': page,
        }
        return self._client.make_request(
            self._base_url,
            ep_alias.GetAliasContactList({'alias_id': alias_id}),
            params=params
        )

    def create_contact(self,
                       alias_id: int,
                       contact_email: str,
                       first_name: str = '',
                       last_name: str = '') -> d_alias.AliasContact:
        data = {
            'contact': contact_email
        }
        if first_name or last_name:
            name = [first_name, last_name]
            name = ' '.join(name)
            data['contact'] = f'{name} <{data["contact"]}>'
        return self._client.make_request(
            self._base_url,
            ep_alias.CreateAliasContact({'alias_id': alias_id}),
            data=data
        )

    def get_mailbox_list(self) -> d_mailbox.MailboxList:
        return self._client.make_request(self._base_url, ep_mailbox.GetMailboxList())

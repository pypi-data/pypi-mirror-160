from simplelogin import BaseClient
from simplelogin.client import ResponseInfo


class TClient(BaseClient):
    """
    Test client doesn't do any network activity,
    instead we add expected response to the list,
    and the client will pretend to receive that
    """
    def __init__(self):
        super().__init__(api_key='')
        self.test_data = []

    def push_response(self, status_code: int, rsp: dict):
        self.test_data.append((status_code, rsp))

    def _make_request_impl(self, method: str, url: str, params: dict, data: dict, headers: dict) -> ResponseInfo:
        scode, data = self.test_data.pop()
        return ResponseInfo(status_code=scode, data=data)
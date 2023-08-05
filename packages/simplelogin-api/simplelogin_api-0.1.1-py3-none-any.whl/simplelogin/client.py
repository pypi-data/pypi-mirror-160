import dataclasses
import typing
from schematics.exceptions import BaseError as SchematicsError
from simplelogin.definitions import Model, Endpoint
from simplelogin import exceptions as exc
from abc import abstractmethod
from urllib.parse import urljoin
import requests
import logging


@dataclasses.dataclass
class ResponseInfo:
    status_code: int
    data: dict


class BaseClient:
    def __init__(self, api_key: str):
        self._api_key = api_key
        self._headers = {
            'Authentication': self._api_key,
            'Content-Type': 'application/json',
        }
        self.logger = logging.getLogger(__name__)

    def make_request(self, base_url: str, ep: Endpoint, params: dict = None, data: dict = None):
        params = self._validate_dict_params(ep.query_type, params)
        data = self._validate_dict_params(ep.data_type, data)
        rsp = self._make_request_impl(ep.method, urljoin(base_url, ep.url), params, data, self._headers)
        if rsp.status_code not in ep.status_code:
            if 200 <= rsp.status_code <= 299:
                self.logger.warning(
                    f'unexpected success status code from ep {ep.url}: '
                    f'got {rsp.status_code}, expected {ep.status_code}'
                )
            else:
                raise exc.ClientError(
                    f'endpoint <{ep.method} {ep.url}> responded with HTTP {rsp.status_code}: {rsp.data}',
                    status_code=rsp.status_code,
                    data=rsp.data)
        self.logger.debug(f'ep: {ep}')
        self.logger.debug(f'params: {params}')
        self.logger.debug(f'data: {data}')
        self.logger.debug(f'rcv: {rsp.data}')
        if ep.rsp_type is not None:
            try:
                model = ep.rsp_type(rsp.data)
                return model
            except SchematicsError as e:
                raise exc.ValidationError(f'error validating response from {ep.url}: {e}')

    def _validate_dict_params(self, model: typing.Type[Model], params: dict):
        if params is not None:
            if model is None:
                raise exc.ValidationError('params passed to undefined model')
            try:
                params_model = model(params)
                return params_model.to_native()
            except SchematicsError as e:
                raise exc.ValidationError(f'error validating params for {model}: {e} with params: {params}')
        return None

    @abstractmethod
    def _make_request_impl(self, method: str, url: str, params: dict, data: dict, headers: dict) -> ResponseInfo:
        pass


class Client(BaseClient):
    def _make_request_impl(self, method: str, url: str, params: dict, data: dict, headers: dict) -> ResponseInfo:
        r = requests.request(
            method,
            url,
            params=params,
            json=data,
            headers=headers,
        )
        if r.headers['Content-Type'] != 'application/json':
            raise exc.ClientError(f'expected Content-Type: application/json, got: {r.headers["Content-Type"]}',
                                  status_code=r.status_code,
                                  data=r.content)
        return ResponseInfo(status_code=r.status_code, data=r.json())

import typing
from schematics import models, types


class Model(models.Model):
    def __init__(self, *args, **kwargs):
        if 'validate' not in kwargs:
            kwargs['validate'] = True
        if 'partial' not in kwargs:
            kwargs['partial'] = False
        super().__init__(*args, **kwargs)
        self.__post_init__(*args, **kwargs)

    def __post_init__(self, *args, **kwargs):
        pass


class EndpointParams(Model):
    def to_native(self, *args, **kwargs):
        obj = super().to_native(*args, **kwargs)  # type: dict
        obj = {k: obj[k] for k in obj.keys() if obj[k] is not None}
        if len(obj) == 0:
            return None
        else:
            return obj


class Endpoint(Model):
    method = types.StringType()
    url = types.StringType()
    status_code = types.IntType()
    query_type: typing.Type[EndpointParams] = None
    data_type: typing.Type[EndpointParams] = None
    rsp_type: typing.Type[Model] = None

    def __str__(self):
        return f'<Endpoint: method: {self.method}, url: {self.url}, status_code: {self.status_code}>'

__all__ = ('LogPoint',)

from expressmoney.api import *

SERVICE = 'auth'


class LogCreateContract(Contract):
    url = serializers.URLField()
    ip = serializers.IPAddressField()
    fingerprint = serializers.CharField(max_length=64, allow_null=True)
    ga = serializers.CharField(max_length=64, allow_null=True)


class LogID(ID):
    _service = SERVICE
    _app = 'users'
    _view_set = 'log'


class LogPoint(CreatePointMixin, ContractPoint):
    _point_id = LogID()
    _create_contract = LogCreateContract

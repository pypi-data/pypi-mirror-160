__all__ = ('BlackListPoint', 'BlackListObjectPoint')

from expressmoney.api import *
from expressmoney.api.point import DestroyPointMixin

SERVICE = 'loans'
APP = 'black_list'


class BlackListCreateContract(Contract):
    comment = serializers.CharField(max_length=128, allow_blank=True)


class BlackListReadContract(Contract):
    created = serializers.DateTimeField()
    user_id = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(max_length=128, allow_blank=True)


class BlackListID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'black_list'


class BlackListPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = BlackListID()
    _read_contract = BlackListReadContract
    _create_contract = BlackListCreateContract


class BlackListObjectPoint(DestroyPointMixin, ContractObjectPoint):
    _point_id = BlackListID()

__all__ = ('BlackListPoint',)

from expressmoney.api import *

SERVICE = 'profiles'
APP = 'black_list'


class BlackListCreateContract(Contract):
    cause = serializers.IntegerField()
    comment = serializers.CharField(max_length=128, allow_blank=True)


class BlackListReadContract(BlackListCreateContract):
    pass


class BlackListID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'black_list'


class BlackListPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = BlackListID()
    _read_contract = BlackListReadContract
    _create_contract = BlackListCreateContract

__all__ = ('UnderwritingTaskPoint', 'BankCardProcessPoint', 'AntifraudProcessPoint')
from expressmoney.api import *

SERVICE = 'profiles'
APP = 'underwriting'


class UnderwritingTaskCreateContract(Contract):
    pass


class BankCardProcessCreateContract(Contract):
    bank_card_id = serializers.IntegerField(min_value=1)
    file = serializers.CharField(max_length=256)


class AntifraudProcessCreateContract(Contract):
    comment = serializers.CharField(max_length=1024)


class UnderwritingTaskID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'underwriting_task'


class BankCardProcessID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'bank_card_process'


class AntifraudProcessID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'antifraudprocess'


class UnderwritingTaskPoint(CreatePointMixin, ContractPoint):
    _point_id = UnderwritingTaskID()
    _create_contract = UnderwritingTaskCreateContract


class BankCardProcessPoint(CreatePointMixin, ContractPoint):
    _point_id = BankCardProcessID()
    _create_contract = BankCardProcessCreateContract


class AntifraudProcessPoint(CreatePointMixin, ContractPoint):
    _point_id = AntifraudProcessID()
    _create_contract = AntifraudProcessCreateContract

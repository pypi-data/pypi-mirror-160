__all__ = ('OrderPoint', 'OrderObjectPoint')

from djmoney.contrib.django_rest_framework import MoneyField
from expressmoney.api import *

SERVICE = 'il'


class OrderCreateContract(Contract):
    requested_period = serializers.IntegerField(min_value=1)
    requested_amount = serializers.IntegerField(min_value=1)
    ip = serializers.IPAddressField()


class OrderReadContract(OrderCreateContract):
    NEW = 'NEW'
    LOAN_CREATED = 'LOAN_CREATED'
    EXPIRED = 'EXPIRED'
    STATUS_CHOICES = (
        (NEW, NEW),
        (LOAN_CREATED, LOAN_CREATED),
        (EXPIRED, EXPIRED),
    )

    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    user_id = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    requested_period = serializers.IntegerField(min_value=1)
    requested_amount = MoneyField(max_digits=7, decimal_places=0)
    approved_period = serializers.IntegerField(min_value=1)
    approved_amount = MoneyField(max_digits=7, decimal_places=0, allow_null=True)
    interest_rate = serializers.DecimalField(max_digits=6, decimal_places=5, allow_null=True)
    score = serializers.DecimalField(max_digits=3, decimal_places=2, allow_null=True)
    sign = serializers.IntegerField(min_value=1)
    contract_demo = serializers.CharField(max_length=256, allow_blank=True)
    ip = serializers.IPAddressField()


class OrderID(ID):
    _service = SERVICE
    _app = 'orders'
    _view_set = 'order'


class OrderPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract
    _create_contract = OrderCreateContract


class OrderObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = OrderID()
    _read_contract = OrderReadContract

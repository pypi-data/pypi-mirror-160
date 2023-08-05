__all__ = ('LoanPoint', 'LoanObjectPoint', 'PaymentPoint', 'EarlyPaymentPoint')

from djmoney.contrib.django_rest_framework import MoneyField
from expressmoney.api import *

SERVICE = 'il'


class LoanCreateContract(Contract):
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    order = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)
    sign = serializers.IntegerField()


class LoanReadContract(Contract):
    ISSUING = 'ISSUING'
    OPEN = 'OPEN'  # Customer received money
    OVERDUE = 'OVERDUE'
    STOP_INTERESTS = 'STOP_INTERESTS'
    CLOSED = 'CLOSED'
    CANCELED = 'CANCELED'
    STATUS_CHOICES = {
        (ISSUING, ISSUING),
        (OPEN, OPEN),
        (OVERDUE, OVERDUE),
        (STOP_INTERESTS, STOP_INTERESTS),
        (CLOSED, CLOSED),
        (CANCELED, CANCELED),
    }
    id = serializers.IntegerField(min_value=1)
    created = serializers.DateTimeField()
    updated = serializers.DateTimeField()
    order = serializers.IntegerField(min_value=1)
    status = serializers.ChoiceField(choices=STATUS_CHOICES)
    bank_card_id = serializers.IntegerField(min_value=1)
    sign = serializers.IntegerField()
    interests_limit = serializers.DecimalField(max_digits=3, decimal_places=2)
    body_issue = MoneyField(max_digits=7, decimal_places=0)
    body_paid = MoneyField(max_digits=7, decimal_places=0)
    body_balance = MoneyField(max_digits=7, decimal_places=0)
    body_debt = MoneyField(max_digits=7, decimal_places=0)
    interests_charges = MoneyField(max_digits=7, decimal_places=0)
    interests_paid = MoneyField(max_digits=7, decimal_places=0)
    interests_balance = MoneyField(max_digits=7, decimal_places=0)


class PaymentCreateContract(Contract):
    loan = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


class EarlyPaymentCreateContract(Contract):
    loan = serializers.IntegerField(min_value=1)
    bank_card_id = serializers.IntegerField(min_value=1)


class LoanID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'loan'


class PaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'payment'


class EarlyPaymentID(ID):
    _service = SERVICE
    _app = 'loans'
    _view_set = 'early_payment'


class LoanPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = LoanID()
    _read_contract = LoanReadContract
    _create_contract = LoanCreateContract


class LoanObjectPoint(RetrievePointMixin, ContractObjectPoint):
    _point_id = LoanID()
    _read_contract = LoanReadContract


class PaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = PaymentID()
    _create_contract = PaymentCreateContract


class EarlyPaymentPoint(CreatePointMixin, ContractPoint):
    _point_id = EarlyPaymentID()
    _create_contract = EarlyPaymentCreateContract


from datetime import date
from decimal import Decimal 
from django.db import transaction
from .models import Transaction, Account, Category

@transaction.atomic
def create_transaction(
    *,
    owner_id: int,
    account_id: int,
    category_id: int,
    kind: str,
    amount: Decimal,
    occurred_at: date,
    description: str = "",
) -> Transaction:
    """
    Docstring for create_transaction
    
    :param owner_id: Description
    :type owner_id: int
    :param account_id: Description
    :type account_id: int
    :param category_id: Description
    :type category_id: int
    :param kind: Description
    :type kind: str
    :param amount: Description
    :type amount: Decimal
    :param occurred_at: Description
    :type occurred_at: date
    :param description: Description, defaults to ""
    :type description: str, optional
    :return: Description
    :rtype: Transaction
    """
    # Validate account and category ownership
    account = Account.objects.get(id=account_id, owner_id=owner_id)
    category = Category.objects.get(id=category_id, owner_id=owner_id)
    
    tx = Transaction.objects.create(
        owner_id=owner_id,
        account=account,
        category=category,
        kind=kind,
        amount=amount,
        occurred_at=occurred_at,
        description=description
    )
    
    return tx


@transaction.atomic
def update_transaction(
    *,
    transaction_instance: Transaction,
    owner_id: int,
    account_id: int,
    category_id: int,
    kind: str,
    amount: Decimal,
    occurred_at: date,
    description: str = "",
) -> Transaction:
    if transaction_instance.owner_id != owner_id:
        raise PermissionError("Owner mismatch for transaction update")

    account = Account.objects.get(id=account_id, owner_id=owner_id)
    category = Category.objects.get(id=category_id, owner_id=owner_id)

    transaction_instance.account = account
    transaction_instance.category = category
    transaction_instance.kind = kind
    transaction_instance.amount = amount
    transaction_instance.occurred_at = occurred_at
    transaction_instance.description = description
    transaction_instance.save(update_fields=[
        "account",
        "category",
        "kind",
        "amount",
        "occurred_at",
        "description",
        "updated_at",
    ])

    return transaction_instance

from datetime import date
from typing import Any

from django.db.models import Sum

from common.utils import month_range
from .models import Transaction

def monthly_summary(*, owner_id: int, ref: date) -> dict[str, Any]:
    """
    Docstring for monthly_summary
    
    :param owner_id: Description
    :type owner_id: int
    :param ref: Description
    :type ref: date
    :return: Description
    :rtype: dict[str, Any]
    """
    start, end = month_range(ref)
    qs = Transaction.objects.filter(owner_id=owner_id, occurred_at__gte=start, occurred_at__lt=end)
    income = qs.filter(kind=Transaction.Kind.INCOME).aggregate(total=Sum("amount"))["total"] or 0
    expense = qs.filter(kind=Transaction.Kind.EXPENSE).aggregate(total=Sum("amount"))["total"] or 0
    balance = income - expense
    
    by_category = (
        qs.filter(kind=Transaction.Kind.EXPENSE)
            .values("category__name")
            .annotate(total=Sum("amount"))
            .order_by("-total")
    )
    
    return {
        "start": start,
        "end": end,
        "income": income,
        "expense": expense,
        "balance": balance,
        "by_category": list(by_category)
    }


def transactions_for_month(*, owner_id: int, ref: date) -> list[Transaction]:
    start, end = month_range(ref)
    return list(
        Transaction.objects.filter(
            owner_id=owner_id,
            occurred_at__gte=start,
            occurred_at__lt=end,
        ).select_related("account", "category").order_by("-occurred_at", "-id")
    )

from django import forms
from .models import Transaction, Account, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "account",
            "category",
            "kind",
            "amount",
            "occurred_at",
            "description",
        ]
        widgets = {
            "occurred_at": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is None:
            return
        self.fields["account"].queryset = Account.objects.filter(owner=user).order_by("name")
        self.fields["category"].queryset = Category.objects.filter(owner=user).order_by("name")

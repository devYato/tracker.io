from django.conf import settings
from django.db import models
from common.models import TimeStampedModel

class Account(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    
    class Meta(TimeStampedModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_account_per_owner")
        ]

    def __str__(self) -> str:
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
class Category(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=60)
    
    class Meta(TimeStampedModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_category_per_owner")
        ]
        
    def __str__(self) -> str:
        return self.name
    
class Transaction(TimeStampedModel):
    class Kind(models.TextChoices):
        INCOME = "IN", "Receita"
        EXPENSE = "OUT", "Despesa"
        
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    kind = models.CharField(max_length=3, choices=Kind.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    occurred_at = models.DateField(db_index=True)
    description = models.CharField(max_length=140, blank=True)
    
    class Meta(TimeStampedModel.Meta):
        indexes = [
            models.Index(fields=["owner", "occurred_at"]),
            models.Index(fields=["owner", "kind", "occurred_at"])
        ]
        
    def __str__(self) -> str:
        return f"{self.Kind(self.kind).label} {self.amount} on {self.occurred_at}"
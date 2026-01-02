from django.contrib import admin
from .models import Account, Category, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_active", "created_at")
    search_fields = ("name", "ownner__username")
    list_filter = ("is_active",)
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "created_at")
    search_fields = ("name", "owner__username")
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "owner", "kind", "amount", "account", "category", "accurred_at")
    list_filter = ("kind", "accurred_at")
    search_fields = ("description", "owner__username", "category__name", "account__name")
    autocomplete_fields = ("account", "category")
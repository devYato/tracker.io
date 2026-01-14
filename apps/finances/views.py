from __future__ import annotations

from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import TransactionForm
from .models import Transaction
from .selectors import monthly_summary, transactions_for_month
from .services import create_transaction, update_transaction

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Exibe o dashboard financeiro do usuário logado."""
    user_id = request.user.pk
    if user_id is None:
        raise ValueError("Authenticated user must have an ID")

    summary = monthly_summary(owner_id=user_id, ref=date.today())
    return render(request, "finances/dashboard.html", {"summary": summary})


def _parse_month(value: str | None, fallback: date) -> date:
    if not value:
        return fallback
    try:
        return datetime.strptime(value, "%Y-%m").date().replace(day=1)
    except ValueError:
        return fallback


class TransactionListView(LoginRequiredMixin, ListView):
    template_name = "finances/transaction_list.html"
    context_object_name = "transactions"

    def get_queryset(self) -> list[Transaction]:
        month_ref = _parse_month(self.request.GET.get("month"), date.today())
        return transactions_for_month(owner_id=self.request.user.id, ref=month_ref)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_ref = _parse_month(self.request.GET.get("month"), date.today())
        context["month_value"] = month_ref.strftime("%Y-%m")
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    template_name = "finances/transaction_form.html"
    form_class = TransactionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = create_transaction(
            owner_id=self.request.user.id,
            account_id=form.cleaned_data["account"].id,
            category_id=form.cleaned_data["category"].id,
            kind=form.cleaned_data["kind"],
            amount=form.cleaned_data["amount"],
            occurred_at=form.cleaned_data["occurred_at"],
            description=form.cleaned_data.get("description", ""),
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("finances:transaction-list")


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "finances/transaction_form.html"
    form_class = TransactionForm
    context_object_name = "transaction"

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = update_transaction(
            transaction_instance=self.get_object(),
            owner_id=self.request.user.id,
            account_id=form.cleaned_data["account"].id,
            category_id=form.cleaned_data["category"].id,
            kind=form.cleaned_data["kind"],
            amount=form.cleaned_data["amount"],
            occurred_at=form.cleaned_data["occurred_at"],
            description=form.cleaned_data.get("description", ""),
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse("finances:transaction-list")


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "finances/transaction_confirm_delete.html"
    context_object_name = "transaction"

    def get_queryset(self):
        return Transaction.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("finances:transaction-list")

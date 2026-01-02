from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .selectors import monthly_summary

@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Exibe o dashboard financeiro do usuário logado."""
    user_id = request.user.pk
    if user_id is None:
        raise ValueError("Authenticated user must have an ID")

    summary = monthly_summary(owner_id=user_id, ref=date.today())
    return render(request, "finances/dashboard.html", {"summary": summary})
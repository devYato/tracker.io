from datetime import date

def month_range(d: date) -> tuple[date, date]:
    """Retorna (primeiro_dia_do_mes, primeiro_dia_do_proximo_mes)."""
    start = d.replace(day=1)
    if start.month == 12:
        nxt = start.replace(year=start.year + 1, month=1)
    else:
        nxt = start.replace(month=start.month + 1)
    return start, nxt

from datetime import datetime


def year(request):
    """Добавляет переменную с текущим годом."""
    today = datetime.today()
    return {
        'year': today.year
    }

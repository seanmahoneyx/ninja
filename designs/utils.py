# utils.py
from datetime import datetime
from django.db.models import Max
from .models import Design

def generate_design_num():
    year = datetime.now().year
    prefix = f"MS{year}"
    last_design = Design.objects.filter(design_num__startswith=prefix).aggregate(
        Max('design_num')
    )['design_num__max']

    if last_design:
        last_num = int(last_design[-4:])
        next_num = last_num + 1
    else:
        next_num = 1

    return f"{prefix}{next_num:04d}"

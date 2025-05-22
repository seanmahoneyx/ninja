from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Max
from django.utils import timezone

STATUS_CHOICES = [
        ('p', 'Pending'),
        ('as', 'Assigned'),
        ('ip', 'In Progress'),
        ('s', 'Sent'),
        ('ap', 'Approved'),
        ('o', 'Ordered'),
    ]


def round_to_4_places(value):
    """Rounds a decimal to 4 decimal places."""
    return Decimal(value).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def generate_design_num():
    """Generates the next unique base design number, ignoring revisions."""
    from .models import Design

    year = datetime.now().year
    prefix = f"MS{year}"

    # Only consider base designs (no parent_design) when determining the next number
    base_designs = Design.objects.filter(
        design_num__startswith=prefix,
        parent_design__isnull=True
    )
    last_design = base_designs.aggregate(Max('design_num'))['design_num__max']

    if last_design:
        try:
            last_num = int(last_design[-4:])
        except ValueError:
            last_num = 0
        next_num = last_num + 1
    else:
        next_num = 1

    return f"{prefix}{next_num:04d}"


def get_next_revision_letter(parent_design):
    """Returns the next revision letter (A, B, C, ...) for a given parent design."""
    existing_letters = parent_design.revisions.values_list('revision_letter', flat=True)
    used_letters = sorted(filter(None, existing_letters))

    if used_letters:
        highest_letter = max(used_letters)
        next_letter = chr(ord(highest_letter) + 1)
    else:
        next_letter = 'A'

    return next_letter


def prepare_design_for_save(instance: 'Design'):
    """
    Handles all logic needed before saving a Design instance:
    - Rounds measurements
    - Generates design number
    - Handles revision suffixes
    - Updates status timestamp
    """
    from .models import Design
    # Round measurements
    if instance.length is not None:
        instance.length = round_to_4_places(instance.length)
    if instance.width is not None:
        instance.width = round_to_4_places(instance.width)
    if instance.depth is not None:
        instance.depth = round_to_4_places(instance.depth)

    # Handle new design
    if not instance.design_num:
        if instance.parent_design:
            # It's a revision
            instance.revision_letter = get_next_revision_letter(instance.parent_design)
            instance.design_num = f"{instance.parent_design.design_num}_{instance.revision_letter}"
        else:
            # Base design
            instance.design_num = generate_design_num()

    # Track status update time
    if instance.pk:
        old = Design.objects.get(pk=instance.pk)
        if old.status != instance.status:
            instance.status_updated_at = timezone.now()
    else:
        instance.status_updated_at = timezone.now()

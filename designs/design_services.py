from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Max

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


def prepare_design_for_save(instance):
    from .models import Design
    from django.utils import timezone

    # Round measurements
    if instance.length is not None:
        instance.length = round_to_4_places(instance.length)
    if instance.width is not None:
        instance.width = round_to_4_places(instance.width)
    if instance.depth is not None:
        instance.depth = round_to_4_places(instance.depth)

    # Handle new design number and revisions
    if not instance.design_num:
        if instance.parent_design:
            # It's a revision
            instance.revision_letter = get_next_revision_letter(instance.parent_design)
            instance.design_num = f"{instance.parent_design.design_num}_{instance.revision_letter}"
        else:
            # Base design
            instance.design_num = generate_design_num()

    # Set design_num_index for sorting
    # For base designs like "MS20250007" → extract last 4 digits
    # For revisions like "MS20250007_A" → extract from base part only

    base_num_part = instance.design_num.split('_')[0]  # "MS20250007"
    try:
        instance.design_num_index = int(base_num_part[-4:])
    except (ValueError, IndexError):
        instance.design_num_index = 0  # fallback if something unexpected

    # Track status update time
    if instance.pk:
        old = Design.objects.get(pk=instance.pk)
        if old.status != instance.status:
            instance.status_updated_at = timezone.now()
    else:
        instance.status_updated_at = timezone.now()
from django.db import models
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime



# Helper function for design_num
def generate_design_num():
    from django.db.models import Max
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

# Design model
class Design(models.Model):
    STATUS_CHOICES = [
        ('p', 'Pending'),
        ('a', 'Assigned'),
        ('i', 'In Progress'),
        ('s', 'Sent'),
        ('a', 'Approved'),
        ('o', 'Ordered'),
    ]

    design_num = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey('customers.Customer', on_delete=models.PROTECT, related_name='customer_designs')
    requesting_rep = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='rep_requests')
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='designer_designs')
    ident = models.CharField(max_length=100)
    style = models.CharField(max_length=100)
    length = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    depth = models.DecimalField(max_digits=10, decimal_places=4)
    blank_size = models.CharField(max_length=100)
    test = models.CharField(max_length=100)
    flute = models.CharField(max_length=100)
    paper = models.TextField()
    ard_required = models.BooleanField(default=False)
    pdf_required = models.BooleanField(default=False)
    eps_required = models.BooleanField(default=False)
    dxf_required = models.BooleanField(default=False)
    cape_required = models.BooleanField(default=False)
    samples_required = models.BooleanField(default=False)
    num_samples_requested = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    # assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='assigned_designs')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='p')
    created_at = models.DateTimeField(auto_now_add=True)

    # Rounding rule for decimals upon save
    def save(self, *args, **kwargs):
        def round4(val):
            return Decimal(val).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)

        if self.length is not None:
            self.length = round4(self.length)
        if self.width is not None:
            self.width = round4(self.width)
        if self.depth is not None:
            self.depth = round4(self.depth)

        if not self.design_num:
            self.design_num = generate_design_num()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.design_num

# DesignAttachment model (for multiple file uploads)
class DesignAttachment(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='design_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.design.design_num}"
from django.db import models
from django.conf import settings
from . import design_services

# Design model
class Design(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    design_num = models.CharField(max_length=20, unique=True, editable=False)
    revision_letter = models.CharField(max_length=1, blank=True, null=True)
    parent_design = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='revisions')
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
    paper = models.CharField(max_length=50)
    ard_required = models.BooleanField(default=False)
    pdf_required = models.BooleanField(default=False)
    eps_required = models.BooleanField(default=False)
    dxf_required = models.BooleanField(default=False)
    cape_required = models.BooleanField(default=False)
    samples_required = models.BooleanField(default=False)
    num_samples_requested = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=design_services.STATUS_CHOICES, default='p')
    status_updated_at = models.DateTimeField(auto_now_add=True)
    

    def save(self, *args, **kwargs):
        design_services.prepare_design_for_save(self)
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
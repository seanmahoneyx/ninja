from django.db import models

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    cust_name = models.CharField(unique=True,max_length=100,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.cust_name
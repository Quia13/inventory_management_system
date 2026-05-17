from django.db import models

# Create your models here.
class Sale(models.Model):
    class Meta:
        db_table = 'sales'

    reference_no = models.CharField(max_length=100, unique=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference_no


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
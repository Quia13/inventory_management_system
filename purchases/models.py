from django.db import models

# Create your models here.
class Purchase(models.Model):
    class Meta:
        db_table = 'purchases'

    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)

    reference_no = models.CharField(max_length=100, unique=True)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference_no
    

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
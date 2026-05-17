from django.db import models
from django.core.validators import MinValueValidator
from django.db.models import Sum, Case, When, IntegerField

# Create your models here.
class Category(models.Model):
    class Meta:
        db_table = 'categories'

    name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    class Meta:
        db_table = 'products'

    product_image = models.ImageField(upload_to='products/', null=True, blank=True)
    product_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    category = models.ForeignKey('inventory.Category', on_delete=models.CASCADE)

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    buying_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    sku = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(max_length=255, blank=True, null=True)

    low_stock_threshold = models.PositiveIntegerField(default=10)
    status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_stock_quantity(self):
        movements = self.stock_movements.all()

        stock_in = movements.filter(movement_type='IN').aggregate(
            total=Sum('quantity')
        )['total'] or 0

        stock_out = movements.filter(movement_type='OUT').aggregate(
            total=Sum('quantity')
        )['total'] or 0

        adjustments = movements.filter(movement_type='ADJ').aggregate(
            total=Sum('quantity')
        )['total'] or 0

        return stock_in - stock_out + adjustments

    def __str__(self):
        return self.product_name
    
class StockMovement(models.Model):
    class Meta:
        db_table = 'stock_movements'

    IN = 'IN'
    OUT = 'OUT'
    ADJUSTMENT = 'ADJ'

    MOVEMENT_TYPE_CHOICES = [
        (IN, 'Stock In'),
        (OUT, 'Stock Out'),
        (ADJUSTMENT, 'Adjustment'),
    ]

    product = models.ForeignKey(
        'inventory.Product',
        on_delete=models.CASCADE,
        related_name='stock_movements'
    )

    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()

    reference = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
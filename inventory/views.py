from decimal import Decimal, InvalidOperation

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, StockMovement
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.conf import settings
# Create your views here.


@login_required
def inventory(request):
    return render(request, 'pages/inventory/index.html')


@login_required
def product(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    data = {
        "categories": categories,
        "products": products
    }
    
    return render(request, 'pages/inventory/product/index.html', data)

@login_required
def add_product(request):
    categories = Category.objects.all()
    errors = []

    if request.method == "POST":
        product_name = request.POST.get("product_name", "").strip()
        description = request.POST.get("description", "").strip()
        category_id = request.POST.get("category")
        selling_price = request.POST.get("selling_price")
        buying_price = request.POST.get("buying_price")
        low_stock_threshold = request.POST.get("low_stock_threshold", 10)
        sku = request.POST.get("sku", "").strip()
        barcode = request.POST.get("barcode", "").strip()
        product_image = request.FILES.get("product_image")

        # Validation
        if not product_name:
            errors.append("Product name is required.")

        if not category_id:
            errors.append("Category is required.")

        # Convert prices safely
        try:
            selling_price = Decimal(selling_price)
            if selling_price < 0:
                errors.append("Selling price must be 0 or higher.")
        except (InvalidOperation, TypeError):
            errors.append("Selling price must be a valid number.")

        try:
            buying_price = Decimal(buying_price)
            if buying_price < 0:
                errors.append("Buying price must be 0 or higher.")
        except (InvalidOperation, TypeError):
            errors.append("Buying price must be a valid number.")

        try:
            low_stock_threshold = int(low_stock_threshold)
            if low_stock_threshold < 0:
                errors.append("Low stock threshold must be 0 or higher.")
        except (ValueError, TypeError):
            errors.append("Low stock threshold must be a valid number.")

        # Get category
        category = None
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                errors.append("Invalid category selected.")

        # Create product
        if not errors:
            try:
                Product.objects.create(
                    product_name=product_name,
                    description=description,
                    category=category,
                    selling_price=selling_price,
                    buying_price=buying_price,
                    low_stock_threshold=low_stock_threshold,
                    sku=sku if sku else None,
                    barcode=barcode if barcode else None,
                    product_image=product_image,
                    status=True
                )
                
                messages.success(request, "Product added successfuly!")
                return redirect("inventory:product")
            
            except IntegrityError:
                errors.append("Product name already exists.")
            except Exception as e:
                errors.append(str(e))

    return render(request, "pages/inventory/product/index.html", {
        "categories": categories,
        "errors": errors
    })


@login_required
def update_product(request, id=None):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'POST':
        try:
            product_name = request.POST.get('product_name')
            category_id = request.POST.get('category')
            description = request.POST.get('description')
            selling_price = request.POST.get('selling_price')
            buying_price = request.POST.get('buying_price')
            low_stock_threshold = request.POST.get('low_stock_threshold')
            sku = request.POST.get('sku')
            barcode = request.POST.get('barcode')
            product_image = request.FILES.get('product_image')
            status = request.POST.get('status') == 'on'  

            product.product_name = product_name
            product.category = Category.objects.get(pk=category_id)
            product.selling_price = selling_price
            product.buying_price = buying_price
            product.low_stock_threshold = low_stock_threshold
            product.status = status

            if product_name != product.product_name:
                product.product_name = product_name
            
            if description:
                product.description = description

            if sku:
                product.sku = sku
        
            if barcode:
                product.barcode = barcode

            if product_image:
                product.product_image = product_image

            product.save()
            messages.success(request, "Product updated successfully.")
            return redirect('inventory:product')

        except IntegrityError as e:
            messages.error(request, "Product name already exists.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return redirect('inventory:product')

@login_required
def delete_product(request, id=None):
    if request.method == 'POST':
        
        try:
            product = Product.objects.get(pk=id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('inventory:product')

        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('inventory:product')

    messages.error(request, "Invalid request method.")
    return redirect('inventory:product')
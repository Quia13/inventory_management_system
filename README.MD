### Installation Process
# make sure to install dependencies if you have not installed yet
- py install Pillow
- py install mysqlclient


## Add data in categories

# run this command
- python manage.py shell

# write this in shell
from inventory.models import Category

# Insert one category
Category.objects.create(name="Electronics")

# Insert multiple categories
Category.objects.create(name="Books")
Category.objects.create(name="Clothing")
Category.objects.create(name="Food")
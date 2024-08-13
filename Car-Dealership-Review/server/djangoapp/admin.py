from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline class
admin.site.register(CarModel)

# CarModelAdmin class
admin.site.register(CarMake)

# CarMakeAdmin class with CarModelInline

# Register models here

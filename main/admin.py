from django.contrib import admin
from main import models 
# Register your models here.
admin.site.register([
    models.Assign,
    models.Employee,
    models.Stock,
    models.Supplier,
    models.Repair,
    models.deletedProductLogs,
    models.repairProductLogs

])
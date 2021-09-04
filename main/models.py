from django.core import validators
from django.db import models
from django.db.models.fields.related import ForeignKey,OneToOneField 
from django.contrib.auth.models import User 
from django.core.validators import MinValueValidator
from datetime import date
from django.core.validators import RegexValidator

# Create your models here.

PROD_CHOICES = (
    ('DESKTOP','DESKTOP'),
    ('KEYBOARD', 'KEYBOARD'),
    ('HDD','HDD'),
    ('SSD','SSD'),
    ('ROUTER','ROUTER'),
    ('MOUSE','MOUSE'),
    ('CPU','CPU'),
    ('LAPTOP','LAPTOP'),
)

class Employee(models.Model):
    emp_id = models.AutoField(primary_key=True)
    sap_number = models.CharField(max_length = 8,unique=True,default="")
    staff_number = models.CharField(max_length = 10,unique=True,default="")
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15,unique=True)
    designation = models.CharField(max_length=50)
    department = models.CharField(max_length=20,default=' ')
    floor = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    desk_num = models.CharField(max_length=20,unique=True)
    

    def __str__(self):
        return self.name 

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='')
    description = models.TextField(default=' ')
    contact = models.CharField(max_length=15,unique=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    department = models.CharField(max_length=100,unique=True)
    hod = models.CharField(max_length=100)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    def __str__(self):
        return str(self.department)

class Stock(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50,default=' ')
    serial_num = models.CharField(max_length=100, unique=True,default=' ')
    specification = models.TextField(default=' ')
    date_received = models.DateField(default=date.today)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.serial_num


class Assign(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50,default=' ')
    serial_num = models.CharField(max_length=100, unique=True,default=' ')
    specification = models.TextField(default=' ')
    date_received = models.DateField(default=date.today)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE,default=1)
    # Will be adding date of assignment also
    emp_id = ForeignKey(Employee,on_delete=models.CASCADE)



class Repair(models.Model):
    prod_id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50,default=' ')
    serial_num = models.CharField(max_length=100, unique=True,default=' ')
    specification = models.TextField(default=' ')
    date_received = models.DateField(default=date.today)
    supplier_id = ForeignKey(Supplier,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.prod_id)


class deletedProductLogs(models.Model):
    id = models.AutoField(primary_key=True)
    prod_name = models.CharField(max_length=50,default=' ')
    serial_num = models.CharField(max_length=100, unique=True,default=' ')
    specification = models.TextField(default=' ')
    date_received = models.DateField()
    date = models.DateField(default=date.today)
    supplier = models.ForeignKey(Supplier,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.serial_num)

class repairProductLogs(models.Model):
    # will declare it 
    pass


##  whenever a new pdt comes it will be added into this table
#  --- Stock => product table 

## Assignment table 
#  --- all fields of product table  + ForeignKey => employee

## Repair table 
#  --- all fields of product table  + ForeignKey => supplier

## Employee 

## DeletedProductLogs

## RepairPdtLogs




# Product Add Form 
# ==> Product Name (Specs make a dropdown) 
# ==> Specifications (Text)
# ==> Date Received 
# ==> Serial Number 
# ==> Want to assign someone


# Employee Table
# ==> emp_id
# ==> name
# ==> contact
# ==> designation
# ==> floor
# ==> desk_num

# Repair_logs
# ==> prod_id 
# ==> vendor_id
# ==> date_sent
# ==> date_recieved

# unusable_pdt_logs
# ==>
# ==>
# ==>



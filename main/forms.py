from django.forms import models
from main.models import Supplier
from django import forms  

DEPARTMENT_CHOICES =( 
    ("HR", "HR"), 
    ("IT", "IT"), 
    ("FINANCE", "FINANCE"), 
    ("PRODUCTION", "PRODUCTION"), 
    ("MARKETING", "MARKETING"), 
) 

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


MIN_FLOOR_VALUE = 0
MAX_FLOOR_VALUE = 5

class addEmployee(forms.Form):
    name = forms.CharField(max_length=20)
    contact = forms.CharField(max_length=12)
    designation = forms.CharField(max_length=20)
    department = forms.ChoiceField(choices = DEPARTMENT_CHOICES)
    desk_num = forms.CharField(max_length=10)
    floor = forms.IntegerField(min_value=MIN_FLOOR_VALUE, max_value=MAX_FLOOR_VALUE)


class addSupplier(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(max_length=256)
    contact = forms.CharField(max_length=15)
        

class addProduct(forms.Form):
    prod_name = forms.ChoiceField(choices = PROD_CHOICES)
    serial_num = forms.CharField(max_length=100)
    specification = forms.CharField(max_length=256)
    date_received = forms.DateField(widget = forms.SelectDateWidget)
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all())


class assignProduct(forms.Form):
    empName = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100)
    department = forms.ChoiceField(choices = DEPARTMENT_CHOICES)
    
from django.forms import models
from main.models import Supplier,Department
from django import forms  
from datetime import date
from main.models import PROD_CHOICES


todays_date = date.today()
year = todays_date.year

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

    name = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Employee's Name"}))
    sap_number = forms.CharField(max_length=8,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"SAP Number"}))
    staff_number = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Staff Number"}))
    contact = forms.RegexField(regex=r'^\+?1?\d{9,15}$',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact : Should be between 9 to 15 digits'}))
    designation = forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Designation'}))
    
    department = forms.ModelChoiceField(queryset=Department.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))

    desk_num = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Desk Number'}))
    floor = forms.IntegerField(min_value=MIN_FLOOR_VALUE, max_value=MAX_FLOOR_VALUE,widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Floor'}))


class addSupplier(forms.Form):
    name = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Supplier's Name"}))
    description = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Description'}))
    # contact = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact'}))
    contact = forms.RegexField(regex=r'^\+?1?\d{9,15}$',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Contact : Should be between 9 to 15 digits'}))
        

class addProduct(forms.Form):
    prod_name = forms.ChoiceField(choices = PROD_CHOICES,widget=forms.Select(attrs={'class':'form-control','placeholder':'Produce type'}))
    serial_num = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Serial Number'}))
    specification = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Specification'}))
    #date_received = forms.DateField(widget = forms.SelectDateWidget( years= range(year,year-10,-1 ),  attrs={'class':'form-control','placeholder':'Specification'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    date_received = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date','class':'form-control','placeholder':'Specification' }))



class assignProduct(forms.Form):
    sap_number = forms.CharField(max_length=8,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'SAP Number'}))
    staff_number = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Staff Number'}))
    
class sendForRepair(forms.Form):
    serial_num = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Serial Number'}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))


class addDepartment(forms.Form):
    department = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Department'}))
    hod = forms.CharField(max_length=256,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'HOD'}))
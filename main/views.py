from datetime import date
from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required 
from main import forms
from main import models
from main.forms import PROD_CHOICES,DEPARTMENT_CHOICES

# Create your views here.
@login_required(login_url='/auth/login')
def index(request):

    employee = models.Employee.objects.all()
    suppliers = models.Supplier.objects.all()
    repair = models.Repair.objects.all()
    stock = models.Stock.objects.all()
    repair = models.Repair.objects.all()
    assigned = models.Assign.objects.all()

    prodList = []
    
    for prod_type in PROD_CHOICES:
        type = prod_type[0]
        numStock = len(models.Stock.objects.filter(prod_name = type))
        numAssigned = len(models.Assign.objects.filter(prod_name = type))
        numRepair = len(models.Repair.objects.filter(prod_name = type))
        prodDict  = {}
        prodDict["pdtType"] = type
        prodDict["numStock"] = numStock
        prodDict["numAssign"] = numAssigned
        prodDict["total"] = numStock+numRepair+numAssigned

        prodList.append(prodDict)

    empList = []
    for department in DEPARTMENT_CHOICES:
        dept = department[0]
        employees = models.Employee.objects.filter(department = dept)
        numEmp = len(employees)
        empDict = {}
        empDict["department"] = dept 
        empDict["numEmp"] = numEmp 
        empList.append(empDict)

    # print(prodList)
    # print(empList)
    print(len(employee))
    sendRepairForm = forms.sendForRepair()
    addEmployeeForm = forms.addEmployee()
    addProductForm = forms.addProduct()
    addSupplierForm = forms.addSupplier()
    context = {
        'employeesDetails' : empList,
        'totalProducts' : len(stock) + len(repair) + len(assigned),
        'numEmp' : len(employee),
        'numSupplier' : len(suppliers),
        'numUnderRepair' : len(repair),
        'productDetails' : prodList,
        'sendRepairForm' : sendRepairForm,
        'addEmployeeForm' : addEmployeeForm,
        'addProductForm' : addProductForm,
        'addSupplierForm' : addSupplierForm

    }
    return render(request,'main/index.html',context)


@login_required(login_url='/auth/login')
def addEmployee(request):
    addEmpForm = forms.addEmployee()
    if request.method == 'POST':
        addEmpForm = forms.addEmployee(request.POST)
        if addEmpForm.is_valid():
            try:
                name = addEmpForm.cleaned_data['name']
                contact = addEmpForm.cleaned_data['contact']
                designation = addEmpForm.cleaned_data['designation']
                department = addEmpForm.cleaned_data['department']
                desk_num = addEmpForm.cleaned_data['desk_num']
                floor = addEmpForm.cleaned_data['floor']

                employee = models.Employee(
                    name = name,
                    contact = contact,
                    designation = designation,
                    department = department,
                    floor = floor,
                    desk_num = desk_num
                )

                employee.save()

                return redirect('index')    
            except:
                return HttpResponse("Some Error Occured")

    return HttpResponse("Some Error Occured")

@login_required(login_url='/auth/login')
def addSupplier(request):
    addSupplierForm = forms.addSupplier()
    if request.method == 'POST':
        addSupplierForm = forms.addSupplier(request.POST)
        if addSupplierForm.is_valid():
            try:
                name = addSupplierForm.cleaned_data['name']
                description = addSupplierForm.cleaned_data['description']
                contact = addSupplierForm.cleaned_data['contact']


                supplier = models.Supplier(
                    name = name,
                    contact = contact,
                    description = description
                )

                supplier.save()
            except:
                return HttpResponse("Some Error Occured")

            return redirect('index')            
    return HttpResponse("Some Error Occured")


@login_required(login_url='/auth/login')
def addProduct(request):
    addPdtForm = forms.addProduct()
    if request.method == 'POST':
        addPdtForm = forms.addProduct(request.POST)
        if addPdtForm.is_valid():
            try:
                prod_name = addPdtForm.cleaned_data['prod_name']
                serial_num = addPdtForm.cleaned_data['serial_num']
                specification = addPdtForm.cleaned_data['specification']
                date_received = addPdtForm.cleaned_data['date_received']
                supplier = addPdtForm.cleaned_data['supplier']


                prod = models.Stock(
                    prod_name = prod_name,
                    serial_num = serial_num,
                    specification = specification,
                    date_received = date_received,
                    supplier = supplier
                )

                prod.save()
                return redirect('index')            
            except:
                return HttpResponse("Some Error Occured")            
    return HttpResponse("Some Error Occured")


@login_required(login_url='/auth/login')
def updateEmployee(request,pk):
    employee = models.Employee.objects.get(pk = pk)
    initial = {
        "name" : employee.name,
        "contact" : employee.contact,
        "designation" : employee.designation,
        "department" : employee.department,
        "floor" : employee.floor,
        "desk_num" : employee.desk_num
    }

    updateEmployeeForm = forms.addEmployee(initial=initial)

    if request.method == "POST":
        if request.POST.get('submit_type') == 'update':
            employee.name = request.POST.get('name')
            employee.contact = request.POST.get('contact')
            employee.designation = request.POST.get('designation')
            employee.department = request.POST.get('department')
            employee.floor = request.POST.get('floor')
            employee.desk_num = request.POST.get('desk_num')

            employee.save()
            return redirect('index') 
        else:
            employee.delete()
            return redirect('index') 


    context = {
        'form' : updateEmployeeForm
    }
    return render(request,'main/updateEmployee.html',context)
    
@login_required(login_url='/auth/login')
def updateSupplier(request,pk):
    supplier = models.Supplier.objects.get(pk = pk)
    initial = {
        "name" : supplier.name,
        "contact" : supplier.contact,
        "description" : supplier.description
    }

    updateSupplierForm = forms.addSupplier(initial=initial)

    if request.method == "POST":
        if request.POST.get('submit_type') == 'update':
            supplier.name = request.POST.get('name')
            supplier.contact = request.POST.get('contact')
            supplier.description = request.POST.get('description')

            supplier.save()
            return redirect('index') 
        else:
            supplier.delete()
            return redirect('index') 

    context = {
        'form' : updateSupplierForm
    }
    return render(request,'main/updateSupplier.html',context)
    

@login_required(login_url='/auth/login')
def deleteProduct(request,pk):
    product = models.Stock.objects.get(pk=pk)
    prod_name = product.prod_name
    serial_num = product.serial_num 
    specification = product.specification
    date_received = product.date_received 
    supplier = product.supplier 

    product.delete()

    product_log = models.deletedProductLogs(
        prod_name = prod_name,
        serial_num = serial_num,
        specification = specification ,
        date_received = date_received,
        supplier = supplier
    )

    product_log.save()

    return redirect('index')

@login_required(login_url='/auth/login')
def showProduct(request,slug):
    if slug == "all":
        stock = models.Stock.objects.all()
        assign = models.Assign.objects.all()
        repair = models.Repair.objects.all()
    else:
        stock = models.Stock.objects.filter(prod_name = slug)
        assign = models.Assign.objects.filter(prod_name = slug)
        repair = models.Repair.objects.filter(prod_name = slug)

    context = {
        "itemType" : slug,
        "stock" : stock,
        "assign" : assign,
        "repair" : repair,
        "assignForm" : forms.assignProduct()
    }

    return render(request,'main/listProduct.html',context)

@login_required(login_url='/auth/login')
def listEmployee(request,slug):
    if slug == 'all':
        employees = models.Employee.objects.all()
        
    else:
        employees = models.Employee.objects.filter(department = slug)

    context = {
        "employees" : employees
    }
    return render(request,'main/listEmployee.html',context)





@login_required(login_url='/auth/login')
def listSupplier(request):
    suppliers = models.Supplier.objects.all()
    context = {
        "suppliers" : suppliers
    }
    return render(request,'main/listSupplier.html',context)

# @login_required(login_url='/auth/login')
# def listRepair(request):
#     pass


@login_required(login_url='/auth/login')
def markRepaired(request,pk):
    product = models.Repair.objects.get(pk=pk)
    prod_name = product.prod_name
    serial_num = product.serial_num
    specification = product.specification
    date_received = product.date_received 
    supplier_id = product.supplier_id 

    product.delete()

    obj = models.Stock(
        prod_name = prod_name,
        serial_num = serial_num,
        specification = specification,
        date_received = date_received,
        supplier = supplier_id
    )

    obj.save()

    return HttpResponse("done")

@login_required(login_url='/auth/login')
def assignProduct(request,pk):
    if request.method == "POST":
        name = request.POST.get('empName')
        department = request.POST.get('department')
        designation = request.POST.get('designation')

        try:
            employee = models.Employee.objects.filter(
                        name = name,
                        department=department,
                        designation=designation)[0]
                    
            
            product = models.Stock.objects.get(pk=pk)
            prod_name = product.prod_name
            serial_num = product.serial_num
            specification = product.specification
            date_received = product.date_received
            supplier = product.supplier

            

            assign = models.Assign(
                    prod_name = prod_name,
                    serial_num = serial_num,
                    specification = specification,
                    date_received = date_received,
                    supplier = supplier,
                    emp_id = employee
                )
            assign.save()
            product.delete()

        except:
            return HttpResponse("Error occured please check if the employee with the given details exists")

        return redirect('index')
        

@login_required(login_url='/auth/login')
def sendForRepair(request):
    if request.method == "POST":
        serial_num = request.POST.get('serial_num')
        supplier = request.POST.get('supplier')

        supplier_obj = models.Supplier.objects.filter(name = supplier)
        if(len(supplier_obj) == 0):
            print("Inside 1st If")
            return HttpResponse("Supplier with this name doesnt exist")

        print(supplier_obj)
        print(type(supplier_obj))
        prod_obj_stock = models.Stock.objects.filter(serial_num=serial_num)
        prod_obj_assign = models.Assign.objects.filter(serial_num=serial_num)

        if(len(prod_obj_stock) != 0):
            print("Inside 2nd If")
            # delete from stock table and move to repair table 
            print(len(prod_obj_stock))
            prod_obj_stock = prod_obj_stock[0]
            prod_name = prod_obj_stock.prod_name 
            serial_num = prod_obj_stock.serial_num 
            specification = prod_obj_stock.specification 
            date_received = prod_obj_stock.date_received 
            
            prod_obj_stock.delete()
            repair_obj = models.Repair(
                prod_name = prod_name,
                serial_num = serial_num,
                specification = specification,
                date_received = date_received,
                supplier_id = supplier_obj[0]
            )

            repair_obj.save()
        elif(len(prod_obj_assign) != 0):
            print("Inside 3rd If")
            # delete from assign table and move to repair table 
            prod_obj_assign = prod_obj_assign[0]
            prod_name = prod_obj_assign.prod_name 
            serial_num = prod_obj_assign.serial_num 
            specification = prod_obj_assign.specification 
            date_received = prod_obj_assign.date_received 
            
            prod_obj_assign.delete() 
            repair_obj = models.Repair(
                prod_name = prod_name,
                serial_num = serial_num,
                specification = specification,
                date_received = date_received,
                supplier_id = supplier_obj[0]
            )

            repair_obj.save()
        else:
            return HttpResponse("Product with Serial Number doesnt exist")
        
        return HttpResponse("Ok")
        
        




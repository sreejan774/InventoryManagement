from datetime import date
from django import forms
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required 
from main import forms
from main import models
from main.forms import PROD_CHOICES

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
    departmentChoices = models.Department.objects.all()
    for d in departmentChoices:
        dept = d.department
        employees = models.Employee.objects.filter(department = dept)
        numEmp = len(employees)
        hod = d.hod
        empDict = {}
        empDict["department"] = dept 
        empDict["numEmp"] = numEmp 
        empDict['HOD'] = hod
        empDict['slug'] = d.slug
        empList.append(empDict)

    # print(prodList)
    # print(empList)
    # print(len(employee))
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
        'addSupplierForm' : addSupplierForm,

    }
    return render(request,'main/index.html',context)


@login_required(login_url='/auth/login')
def addEmployee(request):
    addEmpForm = forms.addEmployee()
    if request.method == 'POST':
        addEmpForm = forms.addEmployee(request.POST)
        if addEmpForm.is_valid():
            # try:
            name = addEmpForm.cleaned_data['name']
            sap_number = addEmpForm.cleaned_data['sap_number']
            staff_number = addEmpForm.cleaned_data['staff_number']
            contact = addEmpForm.cleaned_data['contact']
            designation = addEmpForm.cleaned_data['designation']
            department = addEmpForm.cleaned_data['department']
            desk_num = addEmpForm.cleaned_data['desk_num']
            floor = addEmpForm.cleaned_data['floor']

            employee = models.Employee(
                name = name,
                sap_number = sap_number,
                staff_number = staff_number,
                contact = contact,
                designation = designation,
                department = department.department,
                floor = floor,
                desk_num = desk_num
            )

            employee.save()
            
            return redirect('index')    
            # except:
            #     return HttpResponse("Some Error Occured")

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
                print(date_received)
                
                product1 = models.Stock.objects.filter(serial_num = serial_num)
                product2 = models.Assign.objects.filter(serial_num = serial_num)
                product3 = models.Repair.objects.filter(serial_num = serial_num)

                if(len(product1)!=0 or len(product2)!=0 or len(product3)!=0 ):
                    return HttpResponse("Database already have a product with same serial number")

                if(date_received > date.today()): 
                    return HttpResponse("Please enter a correct date")
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
        "sap_number" : employee.sap_number,
        "staff_number": employee.staff_number,
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
            employee.sap_number = request.POST.get('sap_number')
            employee.staff_number = request.POST.get('staff_number')
            employee.contact = request.POST.get('contact')
            employee.designation = request.POST.get('designation')
            department = request.POST.get('department')
            employee.floor = request.POST.get('floor')
            employee.desk_num = request.POST.get('desk_num')

            deptName = models.Department.objects.get(pk = department).department
            # print(deptName)
            employee.department = deptName

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
        employees = models.Employee.objects.filter(department = slug.replace('-',' '))

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

@login_required(login_url='/auth/login')
def listRepair(request):
    repair = models.Repair.objects.all()
    context = {
        "repair" : repair
    }
    return render(request,'main/listRepair.html',context)



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

    return redirect('index')

@login_required(login_url='/auth/login')
def assignProduct(request,pk):
    if request.method == "POST":
        sap_number = request.POST.get('sap_number')
        staff_number = request.POST.get('staff_number')

        try:
            employee = models.Employee.objects.filter(
                       sap_number = sap_number,
                       staff_number = staff_number
                    )[0]
                    
            
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
        print("Inside if")
        serial_num = request.POST.get('serial_num')
        supplier = request.POST.get('supplier')
        print("serial Num",serial_num)
        print("supplier",supplier)
        product1 = models.Stock.objects.filter(serial_num = serial_num)
        product2 = models.Assign.objects.filter(serial_num = serial_num)
        product3 = models.Repair.objects.filter(serial_num = serial_num)
        if(len(product1)==0 and len(product2) == 0 and len(product3)==0):
            return HttpResponse("Product with given serial number does not exist in database")
        
        prod_name = None
        specification = None 
        date_received = None

        if(len(product3) != 0):
            return HttpResponse("Product with provided serial number is already under repair")
        elif(len(product1) != 0 ):
            prod_obj_stock = product1[0]
            prod_name = prod_obj_stock.prod_name  
            specification = prod_obj_stock.specification 
            date_received = prod_obj_stock.date_received 
            prod_obj_stock.delete()
        
        else:
            prod_obj_assign = product2[0]
            prod_name = prod_obj_assign.prod_name 
            serial_num = prod_obj_assign.serial_num 
            specification = prod_obj_assign.specification 
            date_received = prod_obj_assign.date_received 
            
            prod_obj_assign.delete() 

        supplier = models.Supplier.objects.get(pk=supplier)
        repair_obj = models.Repair(
                prod_name = prod_name,
                serial_num = serial_num,
                specification = specification,
                date_received = date_received,
                supplier_id = supplier
            )
        repair_obj.save()
        return redirect('index')        

    return redirect('index')

@login_required(login_url='/auth/login')
def addDepartment(request):
    addDeptForm = forms.addDepartment()
    if request.method == "POST":
        try:
            department = request.POST.get('department')
            hod = request.POST.get('hod')
            slug = department.replace(' ','-')
            obj = models.Department(
                department = department,
                hod = hod,
                slug = slug
            )
            obj.save()
            return redirect('index')
        except:
            return HttpResponse("Error occured check if the department already exists")
    context = {
        "form" : addDeptForm
    }

    return render(request,'main/addDepartment.html',context)



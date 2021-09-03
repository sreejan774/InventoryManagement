from main.forms import assignProduct
from django.urls import path
from main import views

urlpatterns = [
    path('',views.index,name='index'),
    path('addEmployee/',views.addEmployee,name="addEmployee"),
    path('addSupplier/',views.addSupplier,name="addSupplier"),
    path('addProduct/',views.addProduct,name="addProduct"),
    path('updateEmployee/<int:pk>',views.updateEmployee,name='updateEmployee'),
    path('updateSupplier/<int:pk>',views.updateSupplier,name='updateSupplier'),
    path('deleteProduct/<int:pk>',views.deleteProduct,name='deleteProduct'),
    path('products/<slug:slug>',views.showProduct,name='showProduct'),
    path('listEmployee/<slug:slug>',views.listEmployee,name='listEmployee'),
    path('listRepair',views.listRepair,name="listRepair"),
    path('listSupplier/',views.listSupplier,name='listSupplier'),
    path('markRepaired/<int:pk>',views.markRepaired,name='markRepaired'),
    path('assignProduct/<int:pk>',views.assignProduct,name='assignProduct'),
    path('sendForRepair/',views.sendForRepair,name='sendForRepair'),
    path('addDepartment/',views.addDepartment,name='addDepartment')

]
from django.urls import path

from fixorder import views
from fixorder.views import get_client_data, create_client, typical_work_create, get_typical_work_data

urlpatterns = [
                path('', views.Show_orderlist.as_view(), name='orderlist'),
                path('clientlist/', views.Show_clientlist.as_view(), name='clientlist'),
                path('neworder/', views.AddOrder.as_view(), name='neworder'),
                path('order/<int:pk>/', views.Show_and_edit_order.as_view(), name='order'),
                path('warrantydoc/<int:pk>/', views.Warrantydoc.as_view(), name='warrantydoc'),
                path('commingdoc/<int:pk>/', views.Commingdoc.as_view(), name='commingdoc'),
                path('company/', views.CompanyView.as_view(), name='company'),
                path('delete/<int:pk>/', views.DeleteOrder.as_view(), name='delete'),
                path('editclient/<int:pk>/', views.EditClient.as_view(), name='editclient'),
                path('deleteclient/<int:pk>/', views.DeleteClient.as_view(), name='deleteclient'),
                path('newemployee/', views.CreateEmployee.as_view(), name='newemployee'),
                path('employees/', views.Show_Employees.as_view(), name='employees'),
                path('editemployee/<int:pk>/', views.EditEmployee.as_view(), name='editemployee'),
                path('deleteemployee/<int:pk>/', views.DeleteEmployee.as_view(), name='deleteemployee'),
                path('fireemployee/<int:pk>/', views.FireEmployee.as_view(), name='fireemployee'),
                path('api/typical_work_create/', typical_work_create, name='typical_work_create'),
                path('api/typical_work_data/', get_typical_work_data, name='typical_work_data'),
                path('api/clients/<int:client_id>/', get_client_data, name='get_client_data'),
                path('api/clients/create/', create_client, name='create_client'),



]

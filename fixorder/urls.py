from django.urls import path

from fixorder import views
from fixorder.views import get_client_data

urlpatterns = [
                path('', views.Show_orderlist.as_view(), name='orderlist'),
                path('neworder/', views.AddOrder.as_view(), name='neworder'),
                path('order/<int:pk>/', views.Show_and_edit_order.as_view(), name='order'),
                path('warrantydoc/<int:pk>/', views.Warrantydoc.as_view(), name='warrantydoc'),
                path('commingdoc/<int:pk>/', views.Commingdoc.as_view(), name='commingdoc'),
                path('company/', views.CompanyView.as_view(), name='company'),
                path('delete/<int:pk>/', views.DeleteOrder.as_view(), name='delete'),
                path('api/clients/<int:client_id>/', get_client_data, name='get_client_data'),


]

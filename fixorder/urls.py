from django.urls import path

from fixorder import views

urlpatterns = [
                path('', views.Show_orderlist.as_view(), name='orderlist'),
                path('neworder/', views.AddOrder.as_view(), name='neworder'),
                path('order/<int:pk>/', views.Show_and_edit_order.as_view(), name='order'),

]
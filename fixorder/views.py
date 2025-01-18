from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView

from fixorder.models import Order


class Show_and_edit_order(UpdateView):
#class Show_and_edit_order(PermissionRequiredMixin, UpdateView) #потом добавим вход только при авторизации
    model = Order #в этой модели должен быть определен get_absolute_url
    fields = ['client_name', 'client_phone', 'client_telegram', 'client_viber', 'client_whatsapp',
              'time_demand', 'defect',  'device_password', 'device_exterior', 'initial_price',
              'prepaid', 'notes', 'status', 'work', 'work_price', 'work_warranty', 'work1', 'work_price1', 'work_warranty1',
                   'work2', 'work_price2', 'work_warranty2', 'work3', 'work_price3', 'work_warranty3',
                   'work4', 'work_price4', 'work_warranty4','work5', 'work_price5', 'work_warranty5',
                  'work6', 'work_price6', 'work_warranty6']
    template_name = 'fixorder/show_edit_order.html'
    #context_object_name = 'my_order'
#     success_url = reverse_lazy('.') #трэба вернуться сюда же
    success_url = reverse_lazy('order:pk') #трэба вернуться сюда же
    extra_context = {'title': 'Заказ', 'header': 'Просмотреть/изменить заказ'}

class Show_orderlist(ListView):
    model = Order
    template_name = template_name = 'fixorder/orderlist.html'
    context_object_name = 'my_orders'
    paginate_by = 15
    extra_context = {'title': 'Главная страница', 'header': 'Ваши заказы'}

    # def get_queryset(self):
#         return Order.published.all().select_related('cat') #переопределяем выборку (queryset) для переменной context_object_name/'posts'


# class WomenHome(ListView): #без миксина
#     model = Women
#     template_name = 'women/index.html' #по умолчанию вызывается шаблон <имя приложения>/<имя модели>_list.html наш шаблон другой,  то его можно так переопределить
#     context_object_name = 'posts'  #по умолчанию в шаблон передается коллекция object_list (обычно квирисет из модели), но ее можно так переопределить, переназвать
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'cat_selected': 0,
#     }#extra_context не умеет ловить данные динамически (GET)
#
#     def get_queryset(self):
#         return Women.published.all().select_related('cat') #переопределяем выборку (queryset) для переменной context_object_name/'posts'




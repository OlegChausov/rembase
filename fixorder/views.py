from datetime import datetime

from django.db.models import Q, Sum
from django.http import request
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import UpdateView, ListView, CreateView, TemplateView, DetailView, DeleteView

from fixorder.forms import AddOrderForm
from fixorder.models import Order, OrderStatus, Company


# class Show_and_edit_order(UpdateView):
# #class Show_and_edit_order(PermissionRequiredMixin, UpdateView) #потом добавим вход только при авторизации
#     model = Order #в этой модели должен быть определен get_absolute_url
#     fields = ['client_name', 'client_phone', 'client_telegram', 'client_viber', 'client_whatsapp',
#               'time_demand', 'defect',  'device_password', 'device_exterior', 'initial_price',
#               'prepaid', 'notes', 'status', 'total_price', 'time_away', 'work', 'work_price', 'work_warranty', 'work1', 'work_price1', 'work_warranty1',
#                    'work2', 'work_price2', 'work_warranty2', 'work3', 'work_price3', 'work_warranty3',
#                    'work4', 'work_price4', 'work_warranty4','work5', 'work_price5', 'work_warranty5',
#                   'work6', 'work_price6', 'work_warranty6']
#     template_name = 'fixorder/show_edit_order.html'


class Show_and_edit_order(UpdateView):
    model = Order
    fields = [ 'status', 'client_name', 'client_phone', 'client_phone1', 'client_telegram', 'client_viber', 'client_whatsapp',
              'time_demand', 'device', 'defect',  'device_password', 'device_exterior', 'initial_price',
              'prepaid', 'notes', 'time_away', 'work', 'work_price', 'work_warranty', 'work1', 'work_price1', 'work_warranty1',
                   'work2', 'work_price2', 'work_warranty2', 'work3', 'work_price3', 'work_warranty3',
                   'work4', 'work_price4', 'work_warranty4','work5', 'work_price5', 'work_warranty5',
                  'work6', 'work_price6', 'work_warranty6', 'total_price', 'remain_to_pay', 'conclusion']
    template_name = 'fixorder/show_edit_order.html'
    # success_url = reverse_lazy('orderlist')
    extra_context = {'title': 'Заказ', 'header': 'Просмотреть/изменить заказ'}

    def get_success_url(self):
        return reverse_lazy('order', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)




class Show_orderlist(ListView):
    model = Order
    template_name = 'fixorder/orderlist.html'
    context_object_name = 'my_orders'
    paginate_by = 15
    extra_context = {'title': 'Главная страница', 'header': 'Ваши заказы'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        checky = self.request.GET.get('cb')
        if not checky:
            if query:
                # return Order.objects.filter(client_phone__icontains=query) #должно работать на PosgreSQL
                return Order.objects.filter(
                    Q(client_phone__iregex=query) | Q(device__iregex=query) | Q(client_name__iregex=query) | Q(
                        client_telegram__iregex=query))  # для PosgreSQL можно использовать __icontains
            return super().get_queryset()
        else:
            return Order.objects.filter(status__status='Активен').filter(
                    Q(client_phone__iregex=query) | Q(device__iregex=query) | Q(client_name__iregex=query) | Q(
                        client_telegram__iregex=query))


class AddOrder(CreateView):
    # model = Order
    form_class = AddOrderForm
    # fields = ['client_name', 'client_phone', 'client_telegram', 'client_viber', 'client_whatsapp',
    #           'time_demand', 'defect', 'device_password', 'device_exterior', 'initial_price',
    #           'prepaid', 'notes',]
    template_name = 'fixorder/neworder.html'
    success_url = reverse_lazy('orderlist')
    extra_context = {'title': 'Новый заказ', 'header': 'Добавление заказа'}

class Warrantydoc(DetailView):
    # model = Order
    template_name = "fixorder/warrantydoc.html"
    pk_url_kwarg = 'pk'
    context_object_name = 'wr'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Акт выполненных работ'
        # context["time_away"] = datetime.now()
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Order.objects, pk=self.kwargs[self.pk_url_kwarg])


class Commingdoc(DetailView):
    # model = Order
    template_name = "fixorder/commingdoc.html"
    pk_url_kwarg = 'pk'
    context_object_name = 'cm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Приемная квитанция'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Order.objects, pk=self.kwargs[self.pk_url_kwarg])

class DeleteOrder(DeleteView):
    model = Order
    success_url = "/"
    template_name = "fixorder/confirm_delete.html"

class CompanyView(UpdateView):
    model = Company
    fields = '__all__'
    template_name = 'fixorder/edit_company.html'
    success_url = reverse_lazy('company')
  #  context_object_name = 'form'
    extra_context = {'title': 'Профиль компании'}

    def get_object(self, queryset=None):
        pk=1
        obj = get_object_or_404(Company, pk=pk)
        return obj


class Commingdoc(DetailView):
    # model = Order
    template_name = "fixorder/commingdoc.html"
    pk_url_kwarg = 'pk'
    context_object_name = 'cm'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Приемная квитанция'
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Order.objects, pk=self.kwargs[self.pk_url_kwarg])










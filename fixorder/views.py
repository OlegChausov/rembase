from datetime import datetime

from django.conf.urls import handler404
from django.db.models import Q, Sum, ProtectedError
from django.forms import inlineformset_factory
from django.http import request, JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView, CreateView, TemplateView, DetailView, DeleteView
import json

from fixorder.forms import AddOrderForm, AddClientForm, AddEmployeeForm, WorkForm
from fixorder.models import Order, OrderStatus, Company, Client, Employee, Work, TypicalWork

WorkFormSet = inlineformset_factory(Order, Work, form=WorkForm, extra=1)


def get_client_data(request, client_id):
    client = Client.objects.get(pk=client_id)
    data = {
        'name': client.name,
        'phone': client.phone,
        'telegram': client.telegram,
        'viber': client.viber,
        'whatsapp': client.whatsapp,
    }
    return JsonResponse(data)


@csrf_exempt
def create_client(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        telegram = data.get('telegram')
        viber = data.get('viber')
        whatsapp = data.get('whatsapp')

        # Создание нового клиента
        client = Client.objects.create(
            name=name,
            phone=phone,
            telegram=telegram,
            viber=viber,
            whatsapp=whatsapp
        )

        response_data = {
            'success': True,
            'client': {
                'id': client.id,
                'name': client.name,
                'phone': client.phone,
                'telegram': client.telegram,
                'viber': client.viber,
                'whatsapp': client.whatsapp
            }
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})




@csrf_exempt
def typical_work_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        description = data.get('description')

        # Создание нового клиента
        typicwork = TypicalWork.objects.create(description=description)
        response_data = {
            'success': True,
            'typicwork': {'typicwork': typicwork.id, 'description': typicwork.description}}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

def get_typical_work_data(request):
    if request.method == 'GET':
        data = [('', 'Выбор услуги'), ('new', 'Новая услуга')] + [
            (typical_work.description, typical_work.description) for typical_work in TypicalWork.objects.all()]
        if not TypicalWork.objects.exists():
            return JsonResponse({'error': 'Нет доступных данных'}, status=404)
        return JsonResponse(data, safe=False) # Safe=False обязателен, если в JsonResponse передать не словарь
    return JsonResponse({'error': 'Метод не поддерживается'}, status=405)




WorkFormSet = inlineformset_factory(Order, Work, form=WorkForm, extra=0)
class Show_and_edit_order(UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'fixorder/show_edit_order.html'
    success_url = reverse_lazy('orderlist')
    extra_context = {'title': 'Заказ', 'header': 'Просмотреть/изменить заказ'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["work_formset"] = WorkFormSet(self.request.POST, instance=self.object)
        else:
            context["work_formset"] = WorkFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)  # Сохраняем Order, но ещё не пишем в БД
        self.object.save()  # Теперь сохраняем Order
        context = self.get_context_data()
        work_formset = context["work_formset"]
        if work_formset.is_valid():
            work_formset.instance = self.object
            work_formset.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))  # Если ошибки, перерисуем форму

        return super().form_valid(form)

class Show_clientlist(ListView):
    model = Client
    template_name = 'fixorder/clientlist.html'
    context_object_name = 'my_clients'
    paginate_by =20
    extra_context = {'title': 'Клиенты', 'header': 'Список клиентов'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.replace("\\","")
            return Client.objects.all().exclude(id=1).filter(
                Q(phone__iregex=query) | Q(name__iregex=query) | Q(
                    telegram__iregex=query) | Q(phone1__iregex=query))  # для PosgreSQL можно использовать __icontains


        return super().get_queryset().exclude(id=1)





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
                query = query.replace("\\", "")
                # return Order.objects.filter(client_phone__icontains=query) #должно работать на PosgreSQL
                return Order.objects.filter(
                    Q(order_client__phone__iregex=query) | Q(order_client__name__iregex=query) | Q(
                        order_client__telegram__iregex=query))  # для PosgreSQL можно использовать __icontains
            return super().get_queryset()
        else:
            return Order.objects.filter(status__status="Активен").filter(
                    Q(order_client__phone__iregex=query) | Q(order_client__name__iregex=query) |
            Q(order_client__telegram__iregex=query))




class AddOrder(CreateView):
    form_class = AddOrderForm
    template_name = 'fixorder/neworder.html'
    success_url = reverse_lazy('orderlist')
    extra_context = {'title': 'Новый заказ', 'header': 'Добавление заказа'}


#создаем переменные, куда получаем данные из полей формы, созданных в форме на лету (отсутствуют в модели)
#возможно JS создал клиента через модальное окно (path('api/clients/create/', create_client, name='create_client'))
#то при сохранении основной формы поля будут взяты ОТСЮДА
    def form_valid(self, form):
        client_id = form.cleaned_data.get('client')[0]
        client_name = form.cleaned_data.get('name')
        client_phone = form.cleaned_data.get('phone')
        client_phone1 = form.cleaned_data.get('phone1')
        client_telegram = form.cleaned_data.get('telegram')
        client_viber = form.cleaned_data.get('viber')
        client_whatsapp = form.cleaned_data.get('whatsapp')

        #изменение данных клиента в базе client.objects...
        if client_id:
            client = Client.objects.get(pk=client_id)
            #client.name = client_name
            client.phone = client_phone
            client.phone1 = client_phone1
            client.telegram = client_telegram
            client.viber = client_viber
            client.whatsapp = client_whatsapp
            client.save()
    #поле order_client есть у модели order и как следствие у формы, но мы его не выводим на экран
    #но оно обязательно, поэтому требует что-то подставить, или будет значенеи default
    #поэтому поле order_client конкретного экземпляра формы form.instance заполняется переменной client
            form.instance.order_client = client


        else:
            form.add_error(None, 'Выберите клиента')

        return super().form_valid(form)




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
    pk_url_kwarg = 'pk'
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


class EditClient(UpdateView):
    model = Client
    pk_url_kwarg = 'pk'
    fields = '__all__'
    template_name = 'fixorder/editclient.html'
    success_url = reverse_lazy('clientlist')
    extra_context = {'title': 'Клиент', 'header': 'Просмотреть/редактировать клиента'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object)  # Для проверки, что объект не None
        if self.object:
            context['related_orders'] = Order.objects.filter(order_client=self.object)
        return context


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return super().form_valid(form)



class DeleteClient(DeleteView):
    model = Client
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('clientlist')
    template_name = "fixorder/confirm_delete_client.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.client.exists():  # Исправление: order_set.exists() или related_name используется корректно
            raise ProtectedError("Нельзя удалить клиента, у которого есть связанные заказы.",
                                 self.object.order_set.all())
        return super().delete(request, *args, **kwargs)


class Show_Employees(ListView):
    model = Employee
    template_name = 'fixorder/employeelist.html'
    context_object_name = 'my_employees'
    paginate_by = 20
    extra_context = {'title': 'Работники', 'header': 'Список работников'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        checky = self.request.GET.get('cb')
        if not checky:
            if query:
                query = query.replace("\\", "")
                # return Employee.objects.filter(phone__icontains=query) #должно работать на PosgreSQL
                return Employee.objects.filter(
                    Q(name__iregex=query) | Q(position__iregex=query)) # для PosgreSQL можно использовать __icontains
            return super().get_queryset()
        else:
            return Employee.objects.filter(status=1).filter(
                Q(name__iregex=query) | Q(position__iregex=query))



class CreateEmployee(CreateView):
    form_class = AddEmployeeForm
    template_name = 'fixorder/newemployee.html'
    success_url = reverse_lazy('employees')
    extra_context = {'title': 'Новый работник', 'header': 'Добавление работника'}


class DeleteEmployee(DeleteView):
    model = Employee
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('employees')
    template_name = "fixorder/confirm_delete_employee.html"
    extra_context = {'title': 'Внимание!', 'header': 'Удалить работника'}

class FireEmployee(UpdateView):
    model = Employee
    pk_url_kwarg = 'pk'
    fields = []  # Мы не даём пользователю напрямую редактировать поля через форму
    success_url = reverse_lazy('employees')
    template_name = "fixorder/confirm_fire_employee.html"
    extra_context = {'title': 'Внимание!', 'header': 'Уволить работника'}

    def form_valid(self, form):
        employee = self.get_object()
        employee.status = '3'  # Установка статуса "Не работает"
        employee.save()  # Сохранение изменений
        return HttpResponseRedirect(self.success_url)



class EditEmployee(UpdateView):
    model = Employee
    pk_url_kwarg = 'pk'
    fields = ['name', 'position', 'status']  # Добавляем поле "status"
    template_name = 'fixorder/editemployee.html'
    success_url = reverse_lazy('employees')
    extra_context = {'title': 'Работник', 'header': 'Просмотреть/редактировать работника'}

    def form_valid(self, form):
        obj = form.save(commit=False)  # Получаем объект, но ещё не сохраняем его в базу данных
        if obj.status == '3':  # Если статус "не работает" (или другой код)
            return redirect('fireemployee', pk=obj.pk)  # Перенаправляем на удаление
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context['status'] = dict(self.model.STATUS_CHOICES).get(obj.status)
        context['time_hire'] = obj.time_hire
        context['time_fire'] = obj.time_fire
        context['related_orders'] = Order.objects.filter(executor=self.object)
        return context


class TypicalWorks(ListView):
    model = TypicalWork
    template_name = 'fixorder/typical_work_list.html'
    context_object_name = 'my_works'
    paginate_by = 15
    extra_context = {'title': 'Виды работ', 'header': 'Ваши работы'}

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query = query.replace("\\","")
            return TypicalWork.objects.filter(description__icontains=query)# для PosgreSQL можно использовать __icontains
        return TypicalWork.objects.all()

    def post(self, request, *args, **kwargs):
        # Получаем список ID для удаления
        delete_ids = request.POST.getlist('delete_ids')
        if delete_ids:
            # Удаляем выбранные объекты
            self.model.objects.filter(pk__in=delete_ids).delete()
        # Перенаправляем на тот же список или другую страницу
        return redirect('typical_works')  # Замените 'my_list' на ваше имя URL

class СreateTypicalWork(CreateView):
    model = TypicalWork
    fields = '__all__'
    template_name = 'fixorder/new_typical_work.html'
    success_url = reverse_lazy('typical_works')
    extra_context = {'title': 'Добавить новую работу', 'header': 'Добавление новой работы'}
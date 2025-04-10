from datetime import datetime

from django.conf.urls import handler404
from django.db.models import Q, Sum, ProtectedError
from django.forms import inlineformset_factory
from django.http import request, JsonResponse, HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import UpdateView, ListView, CreateView, TemplateView, DetailView, DeleteView
import json

from fixorder.forms import AddOrderForm, AddClientForm, AddEmployeeForm, WorkForm
from fixorder.models import Order, OrderStatus, Company, Client, Employee, Work, TypicalWork


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



WorkFormSet = inlineformset_factory(Order, Work, form=WorkForm, extra=0)
class Show_and_edit_order(UpdateView):
    model = Order
    fields = '__all__'
    template_name = 'fixorder/show_edit_order.html'
    success_url = reverse_lazy('orderlist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        typical_works = TypicalWork.objects.all()  # Загружаем один раз
        context["typical_works"] = typical_works  # Передаём в контекст
        if self.request.POST:
            context["work_formset"] = WorkFormSet(self.request.POST, instance=self.object,
                                                  form_kwargs={"typical_works": typical_works})
        else:
            context["work_formset"] = WorkFormSet(instance=self.object, form_kwargs={"typical_works": typical_works})
        return context

    def form_valid(self, form):
        # Сохраняем основной объект
        self.object = form.save()

        # Получаем данные формсета
        work_formset = WorkFormSet(self.request.POST, instance=self.object)

        if work_formset.is_valid():
            work_formset.save()  # Сохраняем изменения, включая удаление
            print("🔸 Формсет успешно сохранён.")
        else:
            print("❌ Ошибки в формсете:", work_formset.errors)
            return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)

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
        client_id = form.cleaned_data.get('client')
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

from django.http import JsonResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])  # Только POST-запросы
def add_work(request, order_id):
    """
    Функция для добавления работы к заказу
    """
    # Получаем объект заказа
    order = get_object_or_404(Order, pk=order_id)

    # Получаем данные из POST-запроса
    description = request.POST.get("description", "").strip()
    price = request.POST.get("price", "").strip()
    warranty = request.POST.get("warranty", "").strip()

    # Логирование полученных данных
    print("✅ Полученные данные:", {"description": description, "price": price, "warranty": warranty})

    # Проверка обязательных полей
    if not description:
        return JsonResponse({"error": "Описание услуги обязательно."}, status=400)
    if not price:
        return JsonResponse({"error": "Цена обязательна."}, status=400)

    try:
        # Преобразование цены в Decimal
        price = Decimal(price)
        if price < 0:
            return JsonResponse({"error": "Цена должна быть положительной."}, status=400)
    except:
        return JsonResponse({"error": "Цена должна быть числом."}, status=400)

    # Создание новой работы
    work = Work.objects.create(
        order=order,
        description=description,
        price=price,
        warranty=warranty
    )

    # Логирование успешного создания объекта
    print("✅ Работа создана:", work)

    # Возвращаем успешный ответ
    return JsonResponse({
        "message": "Работа успешно добавлена.",
        "work_id": work.id,
        "description": work.description,
        "price": float(work.price),  # Преобразование для JSON
        "warranty": work.warranty
    })


@csrf_exempt
def delete_work_view(request, work_id):
    """
    Обработка запроса на удаление объекта Work с заданным ID.
    """
    if request.method == "POST":
        try:
            # Получаем объект Work с указанным work_id
            work = get_object_or_404(Work, pk=work_id)
            work.delete()  # Удаляем объект из базы данных
            return JsonResponse({"message": f"Объект с ID {work_id} успешно удалён."}, status=200)
        except Work.DoesNotExist:
            return JsonResponse({"error": "Объект не найден."}, status=404)
    else:
        # Если метод запроса не POST
        return JsonResponse({"error": "Неверный метод запроса."}, status=405)




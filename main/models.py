from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from user.models import User

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название',
                            error_messages={'required': 'Название обязательно для заполнения'})
    code = models.BigIntegerField(unique=True, verbose_name='Код',
                                  error_messages={'unique': "Такой код продукта уже существует в системе",
                                                  'required': 'Код обязателен для заполнения'})
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '('+str(self.code)+') '+self.name
    
    class Meta:
        ordering = ('-id',)

class Country(models.Model):
    name = models.CharField(max_length=200)
    code = models.BigIntegerField()

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

type = ((1, "Грузополучатель"),
        (2, "Грузоотправитель"))

class Client(models.Model):
    clientID = models.IntegerField(verbose_name="ID клиента",
        unique=True, error_messages={'unique': 'Клиент с таким ID уже существует',
                                                                "required": "Поле обязательно для заполнения",},
                                   null=True, blank=True)
    fullname = models.CharField(verbose_name="Полное имя", max_length=200, unique=True,
                                error_messages={'unique': "Такой клиент уже существует",
                                                                             "required": "Поле обязательно для заполнения"})
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='Телефон')
    country = models.ForeignKey(Country, verbose_name="Страна",
                                related_name="cl_country",
                                on_delete=models.CASCADE)
    city = ChainedForeignKey(
        City,
        chained_field="country",
        chained_model_field="country",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        verbose_name='Город')
    type = models.IntegerField(choices=type, verbose_name="Тип")
    inn = models.IntegerField(null=True, blank=True, verbose_name='ИНН')
    okpo = models.CharField(max_length=100, null=True, blank=True, verbose_name='ОКПО')
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name='Код')

    store = models.CharField(max_length=100, blank=True, null=True, verbose_name='рынок')
    row = models.CharField(max_length=100, verbose_name='ряд', null=True, blank=True)
    container = models.CharField(max_length=100, verbose_name='контейнер', null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        if self.clientID:
            return '(' + str(self.clientID) + '), ' + self.fullname
        else:
            return self.fullname

class StoreOfClient(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='город')
    store = models.CharField(max_length=100, verbose_name='рынок')
    row = models.CharField(max_length=100, verbose_name='ряд', null=True, blank=True)
    container = models.CharField(max_length=100, verbose_name='контейнер', null=True, blank=True)
    client_store = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.city.name

class SendersOfClient(models.Model):
    sender = models.ForeignKey("Client", related_name='sender', on_delete=models.CASCADE)
    client_sender = models.ForeignKey("Client", related_name='client_sender', on_delete=models.CASCADE)

class EmployeeRole(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employeeID = models.IntegerField(unique=True, error_messages={'unique': 'ID сотрудника уже существует'}, verbose_name="ID сотрудника")
    role = models.ForeignKey(EmployeeRole, on_delete=models.CASCADE, verbose_name='Должность')
    fullname = models.CharField(max_length=200, unique=True, verbose_name='Полное имя',
                                error_messages={'unique': 'Сотрудник с таким именем уже существует'})
    phone = models.CharField(max_length=15, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=256, verbose_name='Адрес', null=True, blank=True)
    description = models.TextField(verbose_name='Дополнительная информация о сотруднике', null=True, blank=True)
    salary = models.FloatField(verbose_name='Оклад', null=True, blank=True)
    currency = models.ForeignKey('route.Currency', on_delete=models.SET_NULL, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.employeeID) + '), ' + self.fullname

class AgentOfClient(models.Model):
    fullname = models.CharField(max_length=100, verbose_name='Полное имя', unique=True,
                                error_messages={'unique': "Контрагент с таким именем уже существует"})
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='Страна')
    store = models.CharField(max_length=100, verbose_name='Рынок', blank=True, null=True)
    phone = models.CharField(max_length=100, verbose_name='Телефон', blank=True, null=True)
    address = models.CharField(max_length=100, verbose_name='Адрес', blank=True, null=True)
    description = models.TextField(verbose_name='Дополнительная информация о контрагенте', blank=True, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '(' + str(self.pk) + '), ' + self.fullname

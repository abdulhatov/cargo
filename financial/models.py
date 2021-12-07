import datetime
from datetime import date
from django.db import models
from main.models import Client, Employee, AgentOfClient
from user.models import User

class CashBox(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True,
                            error_messages={"unique": "Такая касса уже существует"})
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

type = (
        (1, 'Приходник'),
        (2, 'Расходник'),
    )

class Articles(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название', unique=True,
                            error_messages={"unique": "Такая статья уже существует"})
    type = models.IntegerField(choices=type, verbose_name="Тип")
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

class Salary(models.Model):
    currency = models.ForeignKey('route.Currency', on_delete=models.CASCADE)
    dateFrom = models.DateField(verbose_name='Дата От')
    dateTo = models.DateField(verbose_name='Дата До')
    inspection = models.FloatField(default=12.0)
    packing = models.FloatField(default=36.0)
    loading = models.FloatField(default=15.0)

class SalaryCurrency(models.Model):
    currency = models.ForeignKey('route.Currency', on_delete=models.CASCADE)
    curs = models.FloatField(default=0.0)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)

class SalaryInner(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    debt = models.FloatField(verbose_name='Долг', default=0.0)
    oklad = models.FloatField(verbose_name='оклад', default=0.0)
    premiums = models.FloatField(verbose_name='премии', default=0.0)
    other = models.FloatField(verbose_name='прочее', default=0.0)
    interest = models.FloatField(verbose_name='проценты', default=0.0)
    issuance = models.FloatField(verbose_name='Выдача', default=0.0)
    fine = models.FloatField(verbose_name='Штрафы', default=0.0)
    advance = models.FloatField(verbose_name='Авансы', default=0.0)
    services = models.FloatField(verbose_name='Услуги', default=0.0)
    totalSL = models.FloatField(verbose_name='Итого ЗП', default=0.0)
    remainder = models.FloatField(verbose_name='Остаток', default=0.0)
    total = models.FloatField(verbose_name='итого', default=0.0)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)

class ServicesSalary(models.Model):
    country = models.ForeignKey('route.Direction', on_delete=models.CASCADE, verbose_name='')
    inspection = models.FloatField(default=0.0, verbose_name="досмотр")
    packing = models.FloatField(default=0.0, verbose_name="упаковка")
    loading = models.FloatField(default=0.0, verbose_name="погрузка")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)

type2 = (
        (1, 'Приходник'),
        (2, 'Расходник'),
        (3, 'Платежная ведомость'),
        (4, 'Перемещение')
    )

type3 = (
        (1, 'Приходник клиент'),
        (2, 'Приходник контаргент'),
        (3, 'Приходник разное'),
        (4, 'Расходник сотрудник'),
        (5, 'Расходник контаргент'),
        (6, 'Расходник контаргенту клиента'),
        (7, 'Расходник разное'),
        (8, 'Платежная ведомость контаргент'),
        (9, 'Платежная ведомость сотрудник'),
        (10, 'Перемещение')
    )

class Operations(models.Model):
    date = models.DateTimeField(verbose_name='Дата', default=datetime.datetime.today())
    cash = models.ForeignKey(CashBox, related_name='cash', on_delete=models.CASCADE)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья', null=True, blank=True)
    currency = models.ForeignKey("route.Currency", on_delete=models.CASCADE, verbose_name='Валюта')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    route = models.ForeignKey("route.Route", on_delete=models.CASCADE, blank=True, null=True)

    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    agent = models.ForeignKey(AgentOfClient, on_delete=models.CASCADE, blank=True, null=True)
    various = models.CharField(max_length=50, verbose_name='Разное', blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    agentClient = models.ForeignKey('debits.ClientContrAgents', on_delete=models.CASCADE, blank=True, null=True)
    cash_sender = models.ForeignKey(CashBox, related_name='cash_sender', on_delete=models.CASCADE, blank=True, null=True)
    sum = models.FloatField(default=0.0, blank=True, null=True)
    type = models.IntegerField(choices=type2, verbose_name="Тип")
    type2 = models.IntegerField(choices=type3, null=True)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

class OperationsInner(models.Model):
    check = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)
    route = models.ForeignKey("route.Route", on_delete=models.CASCADE, blank=True, null=True)
    sum = models.FloatField(verbose_name="Сумма", default=0.0)
    article = models.ForeignKey(Articles, on_delete=models.CASCADE, blank=True, null=True)
    count = models.FloatField(default=0.0, blank=True, null=True)
    price = models.FloatField(default=0.0, blank=True, null=True)
    note = models.CharField(max_length=30, blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    agent = models.ForeignKey('main.AgentOfClient', on_delete=models.CASCADE, blank=True, null=True)

    inner = models.ForeignKey(Operations, on_delete=models.CASCADE)
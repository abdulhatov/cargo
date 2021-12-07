from django.db import models
from financial.models import Articles, CashBox
from main.models import Country, Client
from user.models import User
from datetime import date
from route.models import Route

class ClientContrAgents(models.Model):
    fullname = models.CharField(max_length=100, verbose_name="ID клиента",
        unique=True, error_messages={'unique': 'Контрагент с таким именем уже существует', "required": "Поле обязательно для заполнения"})
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    store = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    more_info = models.TextField(null=True, blank=True)
    added_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.fullname


class IncomeDebits(models.Model):
    date = models.DateField(verbose_name='Дата', default=date.today)
    currency = models.ForeignKey("route.Currency", on_delete=models.CASCADE, verbose_name='Валюта')
    wh_article = models.ForeignKey(Articles, on_delete=models.CASCADE, verbose_name='Статья')
    cashBox = models.ForeignKey(CashBox, on_delete=models.CASCADE, verbose_name='Касса')
    agent = models.ForeignKey(ClientContrAgents, on_delete=models.CASCADE, verbose_name='Контаргент')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    sum = models.FloatField(default=0.0)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # ONDOLOT

class IncomeDebitsInner(models.Model):
    check = models.CharField(max_length=100, verbose_name='Чек', null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Рейс')
    sum = models.FloatField(verbose_name='Сумма',
                            error_messages={"required": "Поле обязательно для заполнения"})
    inner = models.ForeignKey(IncomeDebits, on_delete=models.CASCADE)


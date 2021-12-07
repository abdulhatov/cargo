from django.db import models
from financial.models import Articles
from smart_selects.db_fields import ChainedForeignKey

from route.models import Route
from main.models import Client
from datetime import date
from user.models import User

# склад
class AddList(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название', unique=True,
                             error_messages={"unique": "Склад с таким именем уже существует"})
    content = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'список'
        verbose_name_plural = 'списки'

# Категория
class CategoryName(models.Model):
    category_item = [
        ('литр', 'литр'),
        ('штук', 'штук'),
        ('килограмм', 'килограмм')
    ]
    title = models.CharField(max_length=250, verbose_name='Название', unique=True,
                             error_messages={"unique": "Категория к складу с таким именем уже существует"})
    unit = models.CharField(max_length=10, choices=category_item, verbose_name='единица измерений')

    def __str__(self):
        return self.title

# Наимование
class ListName(models.Model):
    title = models.CharField(max_length=250, verbose_name='Название', unique=True,
                             error_messages={"unique": "Такое наименование уже существует"})
    category = models.ForeignKey(CategoryName, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.title

type = (
        (1, 'Приходник'),
        (2, 'Расходник'),
        (3, 'Перемещение')
    )

class WarehouseOperation(models.Model):
    date = models.DateField(verbose_name='Дата', default=date.today)
    warehouse = models.ForeignKey(AddList, related_name='warehouse', on_delete=models.CASCADE)
    wh_article = models.ForeignKey(Articles, on_delete=models.CASCADE, blank=True, null=True)
    from_warehouse = models.ForeignKey(AddList, related_name='from_warehouse', on_delete=models.CASCADE,
                                       blank=True, null=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='ID рейса',
                              blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Клиент',
                               null=True, blank=True)
    sum = models.FloatField(default=0.0)
    type = models.IntegerField(choices=type, verbose_name="Тип")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # ONDOLOT

class WarehouseOperationInner(models.Model):
    category = models.ForeignKey(CategoryName, on_delete=models.CASCADE, verbose_name='Категория')
    name = ChainedForeignKey(ListName, chained_field='category', chained_model_field="category",
                             auto_choose=True, show_all=False)
    sum = models.FloatField(verbose_name='Количество', default=0.0,)
    price = models.FloatField(verbose_name='цена', default=0.0, blank=True, null=True)
    inner = models.ForeignKey(WarehouseOperation, on_delete=models.CASCADE)

# class StockBalance(models.Model):
#     warehouse = models.ForeignKey(AddList, on_delete=models.CASCADE)
#     naming = models.ForeignKey(ListName, on_delete=models.CASCADE)
#     total = models.FloatField(default=0)

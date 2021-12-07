# Generated by Django 3.2 on 2021-11-29 11:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Такая статья уже существует'}, max_length=100, unique=True, verbose_name='Название')),
                ('type', models.IntegerField(choices=[(1, 'Приходник'), (2, 'Расходник')], verbose_name='Тип')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='CashBox',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Такая касса уже существует'}, max_length=100, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2021, 11, 29, 17, 40, 25, 839281), verbose_name='Дата')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('various', models.CharField(blank=True, max_length=50, null=True, verbose_name='Разное')),
                ('sum', models.FloatField(blank=True, default=0.0, null=True)),
                ('type', models.IntegerField(choices=[(1, 'Приходник'), (2, 'Расходник'), (3, 'Платежная ведомость'), (4, 'Перемещение')], verbose_name='Тип')),
                ('type2', models.IntegerField(choices=[(1, 'Приходник клиент'), (2, 'Приходник контаргент'), (3, 'Приходник разное'), (4, 'Расходник сотрудник'), (5, 'Расходник контаргент'), (6, 'Расходник контаргенту клиента'), (7, 'Расходник разное'), (8, 'Платежная ведомость контаргент'), (9, 'Платежная ведомость сотрудник'), (10, 'Перемещение')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperationsInner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.CharField(blank=True, max_length=50, null=True)),
                ('sum', models.FloatField(default=0.0, verbose_name='Сумма')),
                ('count', models.FloatField(blank=True, default=0.0, null=True)),
                ('price', models.FloatField(blank=True, default=0.0, null=True)),
                ('note', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateFrom', models.DateField(verbose_name='Дата От')),
                ('dateTo', models.DateField(verbose_name='Дата До')),
                ('inspection', models.FloatField(default=12.0)),
                ('packing', models.FloatField(default=36.0)),
                ('loading', models.FloatField(default=15.0)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryCurrency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curs', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryInner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('debt', models.FloatField(default=0.0, verbose_name='Долг')),
                ('oklad', models.FloatField(default=0.0, verbose_name='оклад')),
                ('premiums', models.FloatField(default=0.0, verbose_name='премии')),
                ('other', models.FloatField(default=0.0, verbose_name='прочее')),
                ('interest', models.FloatField(default=0.0, verbose_name='проценты')),
                ('issuance', models.FloatField(default=0.0, verbose_name='Выдача')),
                ('fine', models.FloatField(default=0.0, verbose_name='Штрафы')),
                ('advance', models.FloatField(default=0.0, verbose_name='Авансы')),
                ('services', models.FloatField(default=0.0, verbose_name='Услуги')),
                ('totalSL', models.FloatField(default=0.0, verbose_name='Итого ЗП')),
                ('remainder', models.FloatField(default=0.0, verbose_name='Остаток')),
                ('total', models.FloatField(default=0.0, verbose_name='итого')),
            ],
        ),
        migrations.CreateModel(
            name='ServicesSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inspection', models.FloatField(default=0.0, verbose_name='досмотр')),
                ('packing', models.FloatField(default=0.0, verbose_name='упаковка')),
                ('loading', models.FloatField(default=0.0, verbose_name='погрузка')),
            ],
        ),
    ]
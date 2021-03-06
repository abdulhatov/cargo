# Generated by Django 3.2 on 2021-11-29 11:40

import datetime
from django.db import migrations, models
import django.db.models.deletion
import route.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Валюта с таким названием уже существует'}, max_length=200, unique=True, verbose_name='Название')),
                ('code', models.CharField(error_messages={'unique': 'Валюта с таким кодом уже существует'}, max_length=200, unique=True, verbose_name='Код')),
            ],
        ),
        migrations.CreateModel(
            name='Direction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('code', models.CharField(error_messages={'unique': 'Такой код направления уже существует в системе'}, max_length=200, unique=True, verbose_name='Код')),
            ],
        ),
        migrations.CreateModel(
            name='Inspector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Loader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NumberOfPlaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unloading', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Packer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('0', 'За вес (кг)'), ('1', 'Погрузка'), ('2', 'Доотправка'), ('3', 'Большой мешок'), ('4', 'Средний мешок'), ('5', 'Маленький мешок'), ('6', 'Разгузка'), ('7', 'Свой мешок')], default='0', max_length=1, verbose_name='Сервис')),
                ('price', models.FloatField(default=0.0, verbose_name='Цена')),
            ],
        ),
        migrations.CreateModel(
            name='ProductP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bag_number', models.PositiveIntegerField(default=0, validators=[route.models.validate_even])),
                ('weight', models.FloatField(default=0.0)),
                ('count', models.IntegerField(default=0, validators=[route.models.validate_even])),
            ],
        ),
        migrations.CreateModel(
            name='ReceptionTransmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateRT', models.DateTimeField(default=datetime.datetime.now, verbose_name='Дата')),
                ('history', models.BooleanField(default=False)),
                ('paid', models.FloatField(default=0.0)),
                ('remainder', models.FloatField(default=0.0)),
                ('pogr', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Такое место уже существует'}, max_length=200, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
        ),
        migrations.CreateModel(
            name='ServicePrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(choices=[('0', 'За вес (кг)'), ('1', 'Погрузка'), ('2', 'Доотправка'), ('3', 'Большой мешок'), ('4', 'Средний мешок'), ('5', 'Маленький мешок'), ('6', 'Разгузка'), ('7', 'Свой мешок')], default='0', max_length=1)),
                ('count', models.IntegerField(default=0)),
                ('priceIV', models.FloatField(default=0.0)),
                ('status', models.BooleanField()),
                ('id_REC_TRAN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='route.receptiontransmission')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idRoute', models.IntegerField(error_messages={'unique': 'Рейс с таким ID уже существует'}, unique=True, verbose_name='ID рейса')),
                ('currency_Som', models.FloatField(default=0.0, verbose_name='Курс по отношению к сому')),
                ('location', models.CharField(choices=[('F', 'Формируется'), ('O', 'Отправлен'), ('P', 'Прибыл'), ('R', 'Роздан')], default='F', max_length=1, verbose_name='Местоположение')),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='Дата')),
                ('status', models.BooleanField(default=False, verbose_name='Статус')),
                ('control_status', models.BooleanField(default=False, verbose_name='Контрольный статус')),
                ('status_places', models.BooleanField(default=False, verbose_name='Статус количества мест')),
                ('note', models.TextField(blank=True, default='', null=True, verbose_name='Примечание')),
                ('country_recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='route.direction', verbose_name='Страна получатель')),
                ('currency_recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='route.currency', verbose_name='Валюта страны получателя')),
            ],
        ),
    ]

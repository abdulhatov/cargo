from django.db import models
from xdg.Exceptions import ValidationError
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from main.models import Country, Employee, Product, Client
from datetime import datetime, date
from user.models import User

Loc = (
        ('F', 'Формируется'),
        ('O', 'Отправлен'),
        ('P', 'Прибыл'),
        ('R', 'Роздан'),)

# Валюта
class Currency(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True,
                            error_messages={"unique": "Валюта с таким названием уже существует"})
    code = models.CharField(max_length=200, verbose_name='Код', unique=True,
                            error_messages={"unique": "Валюта с таким кодом уже существует"})
    def __str__(self):
        return self.name


# Направление
class Direction(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    code = models.CharField(max_length=200, verbose_name='Код', unique=True,
                            error_messages={"unique": "Такой код направления уже существует в системе"})

    def __str__(self):
        return self.name


# Рейсы
class Route(models.Model):
    idRoute = models.IntegerField(verbose_name='ID рейса', unique=True,
                                  error_messages={"unique": "Рейс с таким ID уже существует"})
    country_recipient = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name='Страна получатель')
    currency_Som = models.FloatField(default=0.0, verbose_name='Курс по отношению к сому')
    currency_recipient = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, verbose_name='Валюта страны получателя')
    location = models.CharField(max_length=1, choices=Loc, default=Loc[0][0], verbose_name='Местоположение')
    date = models.DateTimeField(default=datetime.now, blank=True, verbose_name='Дата') #default=datetime.datetime.now
    status = models.BooleanField(default=False, verbose_name='Статус')
    control_status = models.BooleanField(default=False, verbose_name='Контрольный статус')
    status_places = models.BooleanField(default=False, verbose_name='Статус количества мест')
    note = models.TextField(default="", verbose_name='Примечание', null=True, blank=True)

    def __str__(self):
        return str(str(self.idRoute)+' ('+self.country_recipient.name+')')

class Loader(models.Model):
    name = models.ForeignKey(Employee, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

# Оформление
class Registration(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название', unique=True,
                            error_messages={"unique": "Такое место уже существует"})
    description = models.TextField(verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name
SerV = (
        ('0', 'За вес (кг)'),
        ('1', 'Погрузка'),
        ('2', 'Доотправка'),
        ('3', 'Большой мешок'),
        ('4', 'Средний мешок'),
        ('5', 'Маленький мешок'),
        ('6', 'Разгузка'),
        ('7', 'Свой мешок'),
    )

# Цены сервисов
class ServicePrice(models.Model):
    date = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Дата")

    def __str__(self):
        return self.id.__str__()

# Цены
class Price(models.Model):
    service = models.CharField(max_length=1, choices=SerV, default=SerV[0][0], verbose_name="Сервис")
    country = models.ForeignKey(Direction, on_delete=models.CASCADE, verbose_name="Страна")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Валюта")
    price = models.FloatField(default=0.0, verbose_name="Цена")
    servicePrice = models.ForeignKey(ServicePrice, on_delete=models.CASCADE)

# Прием/передача
class ReceptionTransmission(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='ID рейса')
    sender = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='sender1', verbose_name='Грузоотправитель')
    recipient = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='recipient', verbose_name='Грузополучатель')
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, verbose_name='Место оформления')
    operator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='operators')
    #status = models.BooleanField()
    dateRT = models.DateTimeField(default=datetime.now, verbose_name='Дата')
    history = models.BooleanField(default=False)
    paid = models.FloatField(default=0.0)
    remainder = models.FloatField(default=0.0)
    pogr = models.IntegerField(default=0)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.id.__str__()

# Услуги
class Services(models.Model):
    service = models.CharField(max_length=1, choices=SerV, default=SerV[0][0])
    count = models.IntegerField(default=0)
    priceIV = models.FloatField(default=0.0)
    status = models.BooleanField()
    id_REC_TRAN = models.ForeignKey(ReceptionTransmission, on_delete=models.CASCADE)

# Досмотрщик
class Inspector(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='досмотрщик')
    id_REC_TRAN = models.ForeignKey(ReceptionTransmission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employee', 'id_REC_TRAN',)

    def __str__(self):
        return self.employee.fullname

# Упаковщик
class Packer(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='упаковщик')
    id_REC_TRAN = models.ForeignKey(ReceptionTransmission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('employee', 'id_REC_TRAN',)


def validate_even(value):
    if value == 0:
        raise ValidationError(
            _('Должно быть больше 0'),
            params={'value': value},
        )
# Список Товаров
class ProductP(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bag_number = models.PositiveIntegerField(default=0, validators=[validate_even])
    weight = models.FloatField(default=0.0)
    count = models.IntegerField(default=0, validators=[validate_even])
    recTranID = models.ForeignKey(ReceptionTransmission, on_delete=models.CASCADE)
    def __str__(self):
        return self.product.name

class NumberOfPlaces(models.Model):
    recipient = models.ForeignKey(Client, on_delete=models.CASCADE)
    agent = models.ForeignKey("debits.ClientContrAgents", on_delete=models.CASCADE)
    unloading = models.FloatField(default=0.0)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Userconnection(models.Model):
    userid = models.OneToOneField('UserAccounts', models.DO_NOTHING, db_column='userId', primary_key=True)  # Field name made lowercase.
    providerid = models.CharField(db_column='providerId', unique=True, max_length=255)  # Field name made lowercase.
    provideruserid = models.CharField(db_column='providerUserId', max_length=255)  # Field name made lowercase.
    rank = models.IntegerField(unique=True)
    secret = models.CharField(max_length=255, blank=True, null=True)
    accesstoken = models.CharField(db_column='accessToken', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'UserConnection'
        unique_together = (('userid', 'providerid', 'provideruserid'),)


class Agents(models.Model):
    fullname = models.CharField(unique=True, max_length=255)
    phone = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    country_id = models.SmallIntegerField()
    store = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'agents'


class AgentsOfClients(models.Model):
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    country_id = models.SmallIntegerField()
    store = models.CharField(max_length=45, blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'agents_of_clients'


class Cashbox(models.Model):
    name = models.CharField(unique=True, max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cashbox'


class CashboxArticles(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'cashbox_articles'


class CashboxOperations(models.Model):
    date = models.DateTimeField()
    operation_type = models.SmallIntegerField()
    currency = models.ForeignKey('Currency', models.DO_NOTHING)
    type_id = models.SmallIntegerField()
    description = models.TextField(blank=True, null=True)
    cashbox = models.ForeignKey(Cashbox, models.DO_NOTHING)
    cashbox_from = models.ForeignKey(Cashbox, models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey('Clients', models.DO_NOTHING, blank=True, null=True)
    agent = models.ForeignKey(Agents, models.DO_NOTHING, blank=True, null=True)
    employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
    client_agent = models.ForeignKey(AgentsOfClients, models.DO_NOTHING, blank=True, null=True)
    act = models.ForeignKey('Race', models.DO_NOTHING, blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    operation_id = models.IntegerField()
    manager_id = models.IntegerField()
    main_race = models.ForeignKey('MainRace', models.DO_NOTHING, blank=True, null=True)
    article = models.ForeignKey(CashboxArticles, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cashbox_operations'


class CashboxOperationsInfo(models.Model):
    cashbox_operations = models.ForeignKey(CashboxOperations, models.DO_NOTHING)
    article = models.ForeignKey(CashboxArticles, models.DO_NOTHING, blank=True, null=True)
    sum = models.DecimalField(max_digits=11, decimal_places=2)
    check_info = models.CharField(max_length=255, blank=True, null=True)
    client = models.ForeignKey('Clients', models.DO_NOTHING, blank=True, null=True)
    main_race = models.ForeignKey('MainRace', models.DO_NOTHING, blank=True, null=True)
    count = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
    agent = models.ForeignKey(Agents, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cashbox_operations_info'


class Chat(models.Model):
    user_id = models.BigIntegerField()
    date = models.DateTimeField()
    message = models.CharField(max_length=1024)

    class Meta:
        managed = False
        db_table = 'chat'


class ClientStores(models.Model):
    client = models.ForeignKey('Clients', models.DO_NOTHING)
    city = models.CharField(max_length=45)
    store = models.CharField(max_length=45)
    row = models.CharField(max_length=45, blank=True, null=True)
    container = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client_stores'


class Clients(models.Model):
    client_id = models.IntegerField()
    client_type = models.IntegerField()
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=256, blank=True, null=True)
    city = models.CharField(max_length=45, blank=True, null=True)
    store = models.CharField(max_length=45, blank=True, null=True)
    row = models.CharField(max_length=45, blank=True, null=True)
    container = models.CharField(max_length=45, blank=True, null=True)
    country = models.CharField(max_length=100)
    hwo_create = models.IntegerField()
    last_modified = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    inn = models.CharField(max_length=45, blank=True, null=True)
    okpo = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clients'


class Country(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    code = models.CharField(unique=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'country'


class Currency(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'currency'


class Employees(models.Model):
    fullname = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=45, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)
    type_id = models.SmallIntegerField()
    employee_id = models.IntegerField(unique=True)
    salary = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class MainRace(models.Model):
    race_id = models.IntegerField()
    country = models.ForeignKey(Country, models.DO_NOTHING)
    note = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    kurs = models.DecimalField(max_digits=11, decimal_places=3)
    date = models.DateField()
    admin_status = models.IntegerField(blank=True, null=True)
    foreign_currency = models.ForeignKey(Currency, models.DO_NOTHING)
    places_status = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'main_race'


class MainRaceInvoice(models.Model):
    main_race = models.ForeignKey(MainRace, models.DO_NOTHING)
    contract_date = models.DateField()
    seller = models.CharField(max_length=255)
    buyer = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'main_race_invoice'
        unique_together = (('id', 'main_race'),)


class MainRaceInvoiceInfo(models.Model):
    invoice = models.ForeignKey(MainRaceInvoice, models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    weight_net = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    total_count = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    sum = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    place = models.IntegerField(blank=True, null=True)
    weight_brutto = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_race_invoice_info'
        unique_together = (('id', 'invoice'),)


class MainRaceLading(models.Model):
    race = models.ForeignKey(MainRace, models.DO_NOTHING)
    employee = models.ForeignKey(Employees, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'main_race_lading'


class MainRaceStatus(models.Model):
    race = models.OneToOneField(MainRace, models.DO_NOTHING, primary_key=True)
    status = models.SmallIntegerField()
    user_id = models.IntegerField()
    date_begin = models.DateTimeField(blank=True, null=True)
    date_middle = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_race_status'


class Products(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'products'


class Race(models.Model):
    id = models.BigAutoField(primary_key=True)
    race = models.ForeignKey(MainRace, models.DO_NOTHING)
    date = models.DateTimeField()
    place = models.ForeignKey('RegistationPlace', models.DO_NOTHING)
    sender = models.ForeignKey(Clients, models.DO_NOTHING)
    receiver = models.ForeignKey(Clients, models.DO_NOTHING)
    manager_id = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currency, models.DO_NOTHING)
    kurs = models.DecimalField(max_digits=11, decimal_places=3)
    note = models.TextField(blank=True, null=True)
    receiver_store = models.ForeignKey(ClientStores, models.DO_NOTHING, blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)
    custom_act_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'race'


class RaceAgents(models.Model):
    race = models.ForeignKey(MainRace, models.DO_NOTHING)
    receiver = models.ForeignKey(Clients, models.DO_NOTHING)
    agent = models.ForeignKey(AgentsOfClients, models.DO_NOTHING)
    unload = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'race_agents'


class RaceEmployee(models.Model):
    employee_type = models.SmallIntegerField()
    employee = models.ForeignKey(Employees, models.DO_NOTHING)
    race = models.ForeignKey(Race, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'race_employee'


class RaceProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    bag_number = models.IntegerField()
    count = models.IntegerField()
    weight = models.DecimalField(max_digits=11, decimal_places=2)
    race = models.ForeignKey(Race, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'race_products'


class RaceServices(models.Model):
    id = models.BigAutoField(primary_key=True)
    service_id = models.SmallIntegerField()
    count = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    price_foreign = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    prica_som = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    sum_foreign = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    sum_som = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    race = models.ForeignKey(Race, models.DO_NOTHING)
    paid = models.IntegerField(blank=True, null=True)
    manager_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'race_services'


class ReceiverSenders(models.Model):
    client = models.ForeignKey(Clients, models.DO_NOTHING)
    sender_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'receiver_senders'


class RegistationPlace(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'registation_place'


class Salary(models.Model):
    date_begin = models.DateField()
    date_end = models.DateField()
    cashbox_operation = models.ForeignKey(CashboxOperations, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'salary'


class SalaryInfo(models.Model):
    salary = models.ForeignKey(Salary, models.DO_NOTHING)
    employee = models.ForeignKey(Employees, models.DO_NOTHING)
    debt = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    salary_0 = models.DecimalField(db_column='salary', max_digits=11, decimal_places=2, blank=True, null=True)  # Field renamed because of name conflict.
    premium = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    other = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    persent = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    ru_pack = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    ru_load = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    total_salary = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    advances = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    penalties = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    extradition = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    total = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    kz_pack = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    kz_load = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    kaz_pack = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    avia_pack = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    uz_pack = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    kaz_load = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    avia_load = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)
    uz_load = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'salary_info'


class ServicePrice(models.Model):
    date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'service_price'


class ServicePriceInfo(models.Model):
    entity = models.ForeignKey(ServicePrice, models.DO_NOTHING)
    service_id = models.SmallIntegerField()
    country = models.ForeignKey(Country, models.DO_NOTHING)
    currency = models.ForeignKey(Currency, models.DO_NOTHING)
    price = models.DecimalField(max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_price_info'


class Settings(models.Model):
    key_field = models.CharField(primary_key=True, max_length=45)
    value = models.CharField(max_length=45)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'settings'


class Storage(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'storage'


class StorageItemsCategory(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=45)
    unit_type = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'storage_items_category'


class StorageItemsName(models.Model):
    category = models.ForeignKey(StorageItemsCategory, models.DO_NOTHING)
    name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'storage_items_name'


class StorageOperations(models.Model):
    id = models.IntegerField(primary_key=True)
    storage = models.ForeignKey(Storage, models.DO_NOTHING, db_column='storage')
    storage_from = models.ForeignKey(Storage, models.DO_NOTHING, db_column='storage_from', blank=True, null=True)
    manager = models.ForeignKey('UserAccounts', models.DO_NOTHING)
    act = models.ForeignKey(Race, models.DO_NOTHING, blank=True, null=True)
    article = models.ForeignKey(CashboxArticles, models.DO_NOTHING, blank=True, null=True)
    cashbox_operation = models.ForeignKey(CashboxOperations, models.DO_NOTHING, blank=True, null=True)
    date = models.DateTimeField()
    client = models.ForeignKey(Clients, models.DO_NOTHING, blank=True, null=True)
    race = models.ForeignKey(MainRace, models.DO_NOTHING, blank=True, null=True)
    type = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'storage_operations'


class StorageOperationsInfo(models.Model):
    storage_operations = models.ForeignKey(StorageOperations, models.DO_NOTHING)
    item = models.ForeignKey(StorageItemsName, models.DO_NOTHING, db_column='item')
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    price = models.DecimalField(max_digits=11, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'storage_operations_info'


class UserAccounts(models.Model):
    id = models.BigAutoField(primary_key=True)
    creation_time = models.DateTimeField()
    email = models.CharField(unique=True, max_length=100)
    modification_time = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20)
    sign_in_provider = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=45, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    version = models.BigIntegerField()
    cashbox = models.ForeignKey(Cashbox, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_accounts'

from django.db import models
from django.contrib.auth.models import AbstractUser

class AdvUser(AbstractUser):
    home = models.ManyToManyField('Home')
    is_archive_avaliable = models.BooleanField(help_text= 'Доступ к архиву', verbose_name= 'Доступ к архиву',default= False)
    test_period_until = models.DateTimeField(help_text= 'Тестовый период до',
                                             verbose_name= 'Дата окончания тестового периода', null = True)
    tel_number = models.IntegerField(help_text= 'Введите мобильный телефон', verbose_name= 'Мобильный телефон',null = True)
    is_spam_allowed = models.BooleanField(help_text='Получать уведомления', verbose_name= 'Разрешение уведомлений',
                                          default= False)
    is_activated = models.BooleanField(help_text='Аккаунт прошел активацию', verbose_name= 'Активирован',
                                          default= False)
    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)
    class Meta(AbstractUser.Meta):
        pass

class Home(models.Model):
    index = models.IntegerField(help_text='Введите индекс', verbose_name='Индекс', null= True)
    city = models.CharField(max_length=100, help_text='Введите наименование города', verbose_name='Город', null= True )
    street = models.CharField(max_length=100, help_text='Введите название улицы', verbose_name='Улица', null= True )
    house_number = models.CharField(max_length=100, help_text='Введите номер дома', verbose_name='Номер дома', null= True )
    def __str__(self):
        return str(self.city + ' ' + self.street + ' ' + self.house_number)
    class Meta:
        ordering = ('city',)
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
    def get_absolute_url(self):
        return reverse('address-details', args=[str(self.id)])

class Camera(models.Model):
    linked_home = models.ForeignKey('Home', on_delete=models.CASCADE, null=True)
    is_ok = models.BooleanField(verbose_name='Статус работы')
    is_availiable_places = models.BooleanField(verbose_name='Наличие вободных мест')
    archive_file = models.FileField(verbose_name='Файл архива', blank= True)
    description = models.CharField(max_length=200, help_text='Описание положения камеры', verbose_name='Описание', null=True)
    def __str__(self):
        return str(self.linked_home)
    class Meta:
        ordering = ('is_ok',)
        verbose_name = 'Камера'
        verbose_name_plural = 'Камеры'
    def get_absolute_url(self):
        return reverse('camera-details', args=[str(self.id)])

class Availiable_place(models.Model):
    linked_camera = models.ForeignKey('Camera', on_delete=models.CASCADE, null = True)
    is_actual_status =  models.BooleanField(verbose_name='Статус актуальности')
    distance_to_home = models.FloatField(verbose_name='Расстояние до дома')
    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ('is_actual_status',)
        verbose_name = 'Доступное место'
        verbose_name_plural = 'Доступные места'
    def get_absolute_url(self):
        return reverse('availiable-place-details', args=[str(self.id)])

class Banking_account(models.Model):
    linked_user = models.ForeignKey('AdvUser', on_delete=models.CASCADE, null= True)
    balance = models.FloatField(verbose_name='Доступный баланс')
    account_number = models.IntegerField (verbose_name='Номер счета')
    inn_bank = models.IntegerField (verbose_name='ИНН банка')
    ks_account = models.IntegerField (verbose_name='Корреспонденский счет банка')
    bik_bank = models.IntegerField (verbose_name='БИК банка')
    name_bank = models.CharField(max_length=200, help_text='Введите наименование банка',
                                 verbose_name='Наименование банка')
    auto_payment = models.BooleanField(verbose_name='Автоплатеж')
    def __str__(self):
        return str(self.name_bank + ' ' + str(self.account_number))
    class Meta:
        ordering = ('name_bank',)
        verbose_name = 'Банковские реквизиты'
        verbose_name_plural = 'Банковские реквизиты'
    def get_absolute_url(self):
        return reverse('account-details', args=[str(self.id)])

class Pay_history(models.Model):
    linked_banking_account = models.OneToOneField('Banking_account', on_delete=models.CASCADE)
    actual_date = models.DateTimeField(verbose_name='Последняя дата движения по счету')
    operation_sum = models.FloatField(verbose_name='Сумма операции', default= 0)
    def __str__(self):
        return str(self.linked_banking_account)
    class Meta:
        ordering = ('linked_banking_account',)
        verbose_name = 'Движения по счету'
        verbose_name_plural = 'Движения по счету'
    def get_absolute_url(self):
        return reverse('pay-history-details', args=[str(self.id)])

class Operation(models.Model):
    linked_pay_history = models.ForeignKey('Pay_history', on_delete=models.CASCADE, null= True)
    date = models.DateTimeField(verbose_name='Дата выполнения операции')
    income_balance = models.FloatField(verbose_name='Входящий остаток')
    income_payment = models.FloatField(verbose_name='Поступление')
    outcome_payment = models.FloatField(verbose_name='Списание')
    outcome_balance = models.FloatField(verbose_name='Исходящий остаток')
    def __str__(self):
        return str(self.linked_pay_history)
    class Meta:
        ordering = ('date',)
        verbose_name = 'Операция по счету'
        verbose_name_plural = 'Операции по счету'
    def get_absolute_url(self):
        return reverse('operation-details', args=[str(self.id)])

from django.contrib import admin

from .models import *

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('username','first_name','last_name','tel_number','test_period_until')
    search_fields = ('username',)

class HomeAdmin(admin.ModelAdmin):
    list_display = ('city','street','house_number','index')
    search_fields = ('city',)

class CameraAdmin(admin.ModelAdmin):
    list_display = ('linked_home','is_ok','archive_file')
    list_display_links = ('linked_home',)
    search_fields = ('linked_home',)

class Banking_accountAdmin(admin.ModelAdmin):
    list_display = ('linked_user','name_bank','account_number','balance','auto_payment')
    list_display_links = ('linked_user', )
    search_fields = ('linked_user', )

class Pay_historyAdmin(admin.ModelAdmin):
    list_display = ('linked_banking_account','actual_date','operation_sum')
    list_display_links = ('linked_banking_account',)
    search_fields = ('linked_banking_account',)

class OpearationAdmin(admin.ModelAdmin):
    list_display = ('linked_pay_history','date','outcome_balance',)
    list_display_links = ('linked_pay_history',)
    search_fields = ('linked_pay_history',)

admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Home, HomeAdmin)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Availiable_place)
admin.site.register(Banking_account, Banking_accountAdmin)
admin.site.register(Pay_history, Pay_historyAdmin)
admin.site.register(Operation, OpearationAdmin)


# Register your models here.

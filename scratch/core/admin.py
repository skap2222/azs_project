from django.contrib import admin
from .models import Fuel, Pump, Transaction, Profile

admin.site.site_header = "Панель керування заправкою"
admin.site.site_title = "Адміністратор АЗС"
admin.site.index_title = "Ласкаво просимо до панелі керування"

@admin.register(Fuel)
class FuelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'color_code')
    list_editable = ('price', 'stock', 'color_code')

@admin.register(Pump)
class PumpAdmin(admin.ModelAdmin):
    list_display = ('name', 'fuel', 'status')
    list_filter = ('status', 'fuel')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pump', 'fuel', 'liters', 'amount', 'timestamp', 'is_paid')
    list_filter = ('timestamp', 'fuel', 'is_paid')
    readonly_fields = ('timestamp',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bonus_balance')


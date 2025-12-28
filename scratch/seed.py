import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gas_station.settings')
django.setup()

from core.models import Fuel, Pump

def seed():
    print("Clearing database...")
    Pump.objects.all().delete()
    Fuel.objects.all().delete()

    print("Creating Fuels with specific colors and prices...")
    
    f_100 = Fuel.objects.create(name="100", price=71.99, stock=5000.00, color_code="#28a745") 
    
    f_dp = Fuel.objects.create(name="ДП", price=64.99, stock=8000.00, color_code="#ffc107")
    
    f_95 = Fuel.objects.create(name="95", price=64.99, stock=6000.00, color_code="#dc3545")
    
    f_gas = Fuel.objects.create(name="Газ", price=38.99, stock=4000.00, color_code="#17a2b8")

    print("Creating Pumps...")
    Pump.objects.create(name="Колонка #1", fuel=f_100, status='AVAILABLE')
    Pump.objects.create(name="Колонка #2", fuel=f_95, status='AVAILABLE')
    Pump.objects.create(name="Колонка #3", fuel=f_dp, status='AVAILABLE')
    Pump.objects.create(name="Колонка #4", fuel=f_gas, status='AVAILABLE')
    Pump.objects.create(name="Колонка #5", fuel=f_95, status='BUSY')
    Pump.objects.create(name="Колонка #6", fuel=f_dp, status='OUT_OF_ORDER')

    print("Database seeded successfully with new requirements!")

if __name__ == "__main__":
    seed()

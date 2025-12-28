from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Fuel, Pump, Transaction, Profile
from decimal import Decimal
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
import io
import datetime

try:
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import mm
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Вітаємо, {user.username}! Ваш акаунт створено.")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
@login_required
def profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'core/profile.html', {'profile': user_profile, 'transactions': transactions})

def map_view(request):
    fuels = Fuel.objects.all()
    prices = {fuel.name: float(fuel.price) for fuel in fuels}
    return render(request, 'core/map.html', {'prices': prices})


@login_required
def shop_view(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = int(request.POST.get('price'))
        
        profile = request.user.profile
        
        if profile.bonus_balance >= price:
            profile.bonus_balance -= price
            profile.save()
            messages.success(request, f"Ви успішно придбали {item_name}!")
        else:
            messages.error(request, "Недостатньо бонусів для покупки.")
            
        return redirect('shop')
        
    return render(request, 'core/shop.html')

def promotions_view(request):
    return render(request, 'core/promotions.html')

@login_required
def download_receipt(request, transaction_id):
    if not REPORTLAB_AVAILABLE:
        messages.error(request, "Генерація PDF наразі недоступна (бібліотека не встановлена).")
        return redirect('profile')

    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    y = height - 50 * mm
    
    p.setFont("Helvetica-Bold", 20)
    p.drawString(20*mm, y, "GAS STATION RECEIPT")
    y -= 15*mm
    
    p.setFont("Helvetica", 12)
    p.drawString(20*mm, y, f"Station: Main Branch")
    y -= 8*mm
    p.drawString(20*mm, y, f"Date: {transaction.timestamp.strftime('%d.%m.%Y %H:%M')}")
    y -= 8*mm
    p.drawString(20*mm, y, f"Transaction ID: #{transaction.id}")
    y -= 15*mm
    
    p.line(20*mm, y, 190*mm, y)
    y -= 10*mm
    
    p.drawString(20*mm, y, f"Pump: {transaction.pump.name}")
    y -= 8*mm
    p.drawString(20*mm, y, f"Fuel: {transaction.fuel.name}")
    y -= 8*mm
    p.drawString(20*mm, y, f"Price: {transaction.fuel.price} UAH / L")
    y -= 8*mm
    p.drawString(20*mm, y, f"Volume: {transaction.liters} L")
    y -= 8*mm
    p.setFont("Helvetica-Bold", 14)
    p.drawString(20*mm, y, f"TOTAL: {transaction.amount} UAH")
    y -= 15*mm
    
    p.line(20*mm, y, 190*mm, y)
    y -= 10*mm
    
    p.setFont("Helvetica", 12)
    p.drawString(20*mm, y, f"Bonuses Earned: +{int(transaction.liters)}")
    y -= 20*mm
    
    p.setFont("Helvetica-Oblique", 10)
    p.drawString(20*mm, y, "Thank you for choosing our network!")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=f'receipt_{transaction.id}.pdf')

def index(request):
    pumps = Pump.objects.all()
    fuels = Fuel.objects.all()
    return render(request, 'core/index.html', {'pumps': pumps, 'fuels': fuels})

def fuel_pump(request, pump_id):
    pump = get_object_or_404(Pump, id=pump_id)
    
    if request.method == 'POST':
        try:
            liters_requested = Decimal(request.POST.get('liters', 0))
            if liters_requested <= 0:
                 messages.error(request, "Будь ласка, введіть дійсну кількість літрів.")
                 return redirect('index')

            fuel = pump.fuel
            
            if fuel.stock < liters_requested:
                messages.error(request, f"Недостатньо пального. В наявності: {fuel.stock}л")
                return redirect('index')

            amount = liters_requested * fuel.price
            
            fuel.stock -= liters_requested
            fuel.save()

            transaction = Transaction.objects.create(
                pump=pump,
                fuel=fuel,
                liters=liters_requested,
                amount=amount,
                is_paid=True,
                user=request.user if request.user.is_authenticated else None
            )

            msg = f"Успішно заправлено {liters_requested}л {fuel.name} на суму {amount} грн."
            
            if request.user.is_authenticated:
                profile, created = Profile.objects.get_or_create(user=request.user)
                
                bonuses = int(liters_requested)
                profile.bonus_balance += bonuses
                profile.save()
                msg += f" Нараховано {bonuses} бонусів!"

            messages.success(request, msg)

            if liters_requested >= 20:
                messages.success(request, "COFFEE_PROMO", extra_tags='loyalty_coupon')

            return redirect('index')

        except Exception as e:
            messages.error(request, f"Помилка транзакції: {e}")
            return redirect('index')

    return redirect('index')

from django.db import models
from django.contrib.auth.models import User

class Fuel(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна")
    stock = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Залишок")
    color_code = models.CharField(max_length=7, default='#ffffff', verbose_name="Колір (HEX)")

    def __str__(self):
        return f"{self.name} - ${self.price}"

    class Meta:
        verbose_name = "Пальне"
        verbose_name_plural = "Пальне"

class Pump(models.Model):
    STATUS_CHOICES = [
        ('AVAILABLE', 'Вільна'),
        ('BUSY', 'Зайнята'),
        ('OUT_OF_ORDER', 'Не працює'),
    ]
    name = models.CharField(max_length=50, verbose_name="Назва/Номер")
    fuel = models.ForeignKey(Fuel, on_delete=models.CASCADE, related_name='pumps', verbose_name="Тип пального")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE', verbose_name="Статус")

    def __str__(self):
        return f"{self.name} ({self.fuel.name})"

    class Meta:
        verbose_name = "Колонка"
        verbose_name_plural = "Колонки"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Користувач")
    pump = models.ForeignKey(Pump, on_delete=models.SET_NULL, null=True, verbose_name="Колонка")
    fuel = models.ForeignKey(Fuel, on_delete=models.SET_NULL, null=True, verbose_name="Пальне")
    liters = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Літри")
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Сума")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Час")
    is_paid = models.BooleanField(default=True, verbose_name="Оплачено")

    def __str__(self):
        return f"Транзакція {self.id}"

    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Користувач")
    bonus_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Бонусний баланс")

    def __str__(self):
        return f"{self.user.username} - {self.bonus_balance} бонусів"

    class Meta:
        verbose_name = "Профіль"
        verbose_name_plural = "Профілі"

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

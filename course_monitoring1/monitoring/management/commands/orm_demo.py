from datetime import date
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction
from django.db.models import Avg, Count
from django.db.models.deletion import ProtectedError
from django.utils import timezone
from monitoring.models import Device, Measurement, Passport

class Command(BaseCommand):
    def handle(self, *args, **options):
        devices = Device.objects.filter(serial__in=["V18-A", "V18-B", "V18-C"])
        values = Measurement.objects.filter(device__in=devices)
        print("Середня:", values.aggregate(mean=Avg("temperature")))
        print("Кількість і середнє:", list(devices.annotate(n=Count("measurements"), mean=Avg("measurements__temperature")).values("serial", "n", "mean")))
        print("Мітка Друк:", list(devices.filter(tags__name="Друк").distinct().values_list("serial", flat=True)))
        print("Понад 42:", list(values.filter(temperature__gt=42).values_list("device__serial", "temperature")))
        print("Пристрій A:", values.filter(device__serial="V18-A").count())
        print("Діапазон 32–40:", values.filter(temperature__range=(32, 40)).count())
        print("Дата:", values.filter(measured_at__date=date(2026, 10, 18)).count())
        a = devices.get(serial="V18-A")
        print("get:", a, "filter:", list(devices.filter(serial="V18-A")))
        with transaction.atomic():
            d = Device.objects.create(name="Демонстрація", serial="DEMO-L17")
            Passport.objects.create(device=d, location="Демонстрація")
            m = Measurement.objects.create(device=d, temperature=Decimal("20"), measured_at=timezone.now())
            Measurement.objects.create(device=d, temperature=Decimal("30"), measured_at=timezone.now())
            print("Навчальне середнє:", d.measurements.aggregate(mean=Avg("temperature")), "не менше 25:", d.measurements.filter(temperature__gte=25).count())
            m.temperature = Decimal("25")
            m.save()
            m.refresh_from_db()
            print("Після зміни:", m.temperature)
            m.delete()
            print("Після видалення:", d.measurements.count())
            try:
                d.delete()
            except ProtectedError:
                print("PROTECT:", Device.objects.filter(pk=d.pk).exists(), d.measurements.count())
            for v in ("-80", "150", "151"):
                obj = Measurement(device=d, temperature=Decimal(v), measured_at=timezone.now())
                try:
                    obj.full_clean()
                    print("Валідація:", v, "OK")
                except ValidationError:
                    print("ValidationError:", v)
            try:
                with transaction.atomic():
                    Measurement.objects.create(device=d, temperature=Decimal("151"), measured_at=timezone.now())
            except IntegrityError:
                print("CheckConstraint: IntegrityError")
            d.measurements.all().delete()
            passport_pk = d.passport.pk
            d.delete()
            print("CASCADE: паспорт існує?", Passport.objects.filter(pk=passport_pk).exists())
            transaction.set_rollback(True)
        print("Вимірювань профілю після демонстрації:", values.count())

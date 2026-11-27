import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from monitoring.models import Device, Passport, Tag, Measurement

class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        p = json.loads((Path(settings.BASE_DIR) / "profile18.json").read_text(encoding="utf-8"))
        devices = {}
        for row in p["devices"]:
            device, _ = Device.objects.update_or_create(serial=row["serial"], defaults={"name": row["name"]})
            devices[device.serial] = device
        for row in p["passports"]:
            Passport.objects.update_or_create(device=devices[row["serial"]], defaults={"location": row["location"]})
        tags = {name: Tag.objects.get_or_create(name=name)[0] for name in p["tags"]}
        for serial, names in p["device_tags"].items():
            devices[serial].tags.set([tags[name] for name in names])
        for row in p["measurements"]:
            device = devices[row["serial"]]
            moment = datetime.fromisoformat(row["measured_at"])
            temperature = Decimal(row["temperature"])
            obj, _ = Measurement.objects.get_or_create(device=device, measured_at=moment, temperature=temperature)
            obj.full_clean()
        self.stdout.write(self.style.SUCCESS("Профіль 18 завантажено"))

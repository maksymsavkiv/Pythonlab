from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    name = models.CharField(max_length=80)
    serial = models.CharField(max_length=40, unique=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="devices")

    def __str__(self):
        return f"{self.name} ({self.serial})"

class Passport(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="passport")
    location = models.CharField(max_length=100)

class Measurement(models.Model):
    device = models.ForeignKey(Device, on_delete=models.PROTECT, related_name="measurements")
    temperature = models.DecimalField(max_digits=5, decimal_places=2,
        validators=[MinValueValidator(-80), MaxValueValidator(150)])
    measured_at = models.DateTimeField()

    class Meta:
        ordering = ["-measured_at", "-pk"]
        constraints = [models.CheckConstraint(
            condition=models.Q(temperature__gte=-80, temperature__lte=150),
            name="temperature_in_range")]

from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from .models import Device

@override_settings(ALLOWED_HOSTS=["testserver", "localhost", "127.0.0.1"])
class DeviceTests(TestCase):
    def setUp(self):
        self.device = Device.objects.create(name="Принтер стіл", serial="V18-A")
        Device.objects.create(name="Принтер шафа", serial="V18-B")
        Device.objects.create(name="Офіс", serial="V18-C")

    def test_pages_and_methods(self):
        self.assertEqual(self.client.get(reverse("monitoring:index")).status_code, 200)
        detail = reverse("monitoring:detail", args=[self.device.pk])
        self.assertContains(self.client.get(detail), "V18-A")
        self.assertEqual(self.client.get(reverse("monitoring:detail", args=[999999])).status_code, 404)
        self.assertEqual(self.client.post(detail).status_code, 405)
        self.assertEqual(self.client.post(reverse("monitoring:index")).status_code, 405)

    def test_search(self):
        for q, expected in [("Принтер", ["V18-A", "V18-B"]), ("", ["V18-A", "V18-B", "V18-C"]), ("неіснуючий-зразок", [])]:
            response = self.client.get(reverse("monitoring:index"), {"q": q})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(list(response.context["devices"].values_list("serial", flat=True)), expected)
        self.assertEqual(Device.objects.count(), 3)

    def test_empty(self):
        Device.objects.all().delete()
        self.assertContains(self.client.get(reverse("monitoring:index")), "Пристроїв немає")

    def test_unique_serial(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Device.objects.create(name="Дублікат", serial="V18-A")
        self.assertEqual(Device.objects.count(), 3)

    def test_admin_access(self):
        user = get_user_model().objects.create_user(username="viewer")
        self.client.force_login(user)
        self.assertRedirects(self.client.get(reverse("admin:index")), "/admin/login/?next=/admin/")
        admin = get_user_model().objects.create_superuser(username="labadmin")
        self.client.force_login(admin)
        self.assertEqual(self.client.get(reverse("admin:monitoring_device_changelist")).status_code, 200)

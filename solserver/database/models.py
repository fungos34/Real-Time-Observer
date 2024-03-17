from django.db import models
from django.contrib.auth.models import User


class ProductData(models.Model):
    """Product Details."""
    serial_number = models.CharField(max_length=4, primary_key=True)
    software_version = models.CharField(max_length=6)
    country = models.CharField(max_length=2)
    postcode = models.CharField(max_length=4)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    manufacturing_date = models.DateTimeField(auto_now_add=True)


class StatusData(models.Model):
    """Current SolMate Status."""
    power_income = models.FloatField(null=True)
    power_inject = models.FloatField(null=True)
    power_consumption = models.FloatField(null=True)
    battery = models.FloatField(null=True)
    last_status_update = models.DateTimeField(auto_now=True, null=True)


class SolMate(ProductData, StatusData):
    """Model SolMate."""
    solmate_version = models.CharField(max_length=30, default='v1')
    pv_connectors = models.IntegerField(default=1)
    local_time = models.DateTimeField(null=True)

    def __str__(self):
        """Returns proper string representation."""
        return f"{self.serial_number} {self.owner.username}"




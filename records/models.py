from uuid import uuid4
import uuid
from django.db import models

# Create your models here.
class ReceiptWrite(models.Model):
    REC_ORGN = "REC-ORGN"
    DPRT_ORGN = "DPRT-ORGN"
    ARVD_DSTN = "ARVD-DSTN"
    REC_DSTN = "REC-DSTN"

    STATUS = [
        ("REC-ORGN", "Received at origin"),
        ("DPRT-ORGN", "Departed from origin"),
        ("ARVD-DSTN", "Arrived at destination"),
        ("REC-DSTN", "Received at destination"),
    ]

    no = models.CharField(max_length=36, null=False)
    weight = models.FloatField(null=False)
    count = models.PositiveIntegerField(null=False, default=1)

    sender = models.CharField(max_length=255, null=False)
    _to = models.CharField(max_length=255, null=False)
    addr_ship_from = models.CharField(max_length=255, null=False)
    addr_ship_to = models.CharField(max_length=255, null=False)
    postal_origin = models.PositiveIntegerField(null=False)
    postal_destination = models.PositiveIntegerField(null=False)
    city_origin = models.PositiveIntegerField(null=False)
    city_destination = models.PositiveIntegerField(null=False)
    phone_sender = models.CharField(max_length=16, null=False)
    phone_destination = models.CharField(max_length=16, null=False)
    service_code = models.CharField(max_length=255, default="YES")

    cost = models.PositiveIntegerField(null=False, default=8000)

    status = models.CharField(max_length=255, choices=STATUS, null=False)

    datetime = models.DateTimeField(null=False, auto_now=True)


class ReceiptInstance(models.Model):
    no = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    service_code = models.CharField(max_length=255, default="YES")

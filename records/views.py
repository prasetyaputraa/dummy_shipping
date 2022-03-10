from django.db import transaction
from rest_framework import viewsets, serializers, response, status
from rest_framework.exceptions import ParseError

from .models import ReceiptInstance, ReceiptWrite


class RecordSerializer(serializers.ModelSerializer):
    no = serializers.UUIDField(allow_null=False)
    weight = serializers.FloatField(allow_null=False)
    count = serializers.IntegerField(allow_null=False, default=1)

    sender = serializers.CharField(allow_null=False, max_length=255)
    _to = serializers.CharField(allow_null=False, max_length=255)
    addr_ship_from = serializers.CharField(allow_null=False, max_length=255)
    addr_ship_to = serializers.CharField(allow_null=False, max_length=255)
    postal_origin = serializers.IntegerField(allow_null=False)
    postal_destination = serializers.IntegerField(allow_null=False)
    city_origin = serializers.IntegerField(allow_null=False)
    city_destination = serializers.IntegerField(allow_null=False)
    phone_sender = serializers.CharField(allow_null=False)
    phone_destination = serializers.CharField(allow_null=False)
    service_code = serializers.CharField(allow_null=False)

    cost = serializers.IntegerField(allow_null=False)

    status = serializers.CharField(allow_null=False, max_length=255)

    datetime = serializers.DateTimeField(allow_null=True, read_only=True)

    class Meta:
        model = ReceiptWrite
        fields = "__all__"

    # def create(self, validated_data):
    #     return ReceiptWrite.objects.create(**validated_data)


# Create your views here.
class RecordsViewSet(viewsets.ViewSet):
    def get(self, request, pk):
        receipt_no = ReceiptInstance.objects.get(pk=pk)

        records = ReceiptWrite.objects.filter(no=str(receipt_no.no)).order_by(
            "datetime"
        )

        return response.Response(
            [RecordSerializer().to_representation(record) for record in records],
            status=status.HTTP_200_OK,
        )

    def list(self, request):
        receipts = ReceiptInstance.objects.raw(
            """SELECT t1.* FROM records_receiptwrite as t1
	                JOIN
                    (SELECT no, MAX(datetime) as datetime
		                FROM records_receiptwrite
		                GROUP BY no
	                ) as t2
		                ON t1.no = t2.no
                        WHERE t1.datetime = t2.datetime
                        ORDER BY t1.datetime DESC;"""
        )

        return response.Response(
            [RecordSerializer().to_representation(receipt) for receipt in receipts],
            status=status.HTTP_200_OK,
        )

    @transaction.atomic
    def create(self, request, **kwargs):
        if not request.data.get("service_code"):
            raise ParseError(detail={"service_code": "This field was needed"})

        receipt_no = ReceiptInstance.objects.create(
            service_code=request.data.get("service_code")
        )

        _data = {**request.data}
        _data["_to"] = _data.pop("to")

        record = RecordSerializer(
            data={
                **_data,
                "no": str(receipt_no.no),
                "status": ReceiptWrite.REC_ORGN,
                "datetime": None,
            }
        )
        record.is_valid(raise_exception=True)
        record.save()

        return response.Response(
            record.to_representation(record.instance),
            status=status.HTTP_201_CREATED,
        )

    @transaction.atomic
    def update(self, request, pk):
        receipt_no = ReceiptInstance.objects.get(pk=pk)

        action = request.data.get("action")

        if not action in ("next", "prev"):
            raise ValueError("action must be either next or prev")

        receipts = ReceiptWrite.objects.filter(no=str(receipt_no.no)).order_by(
            "-datetime"
        )
        receipt = receipts[0]

        if (action == "prev") and (receipt.status == ReceiptWrite.REC_ORGN):
            raise ValueError()
        if receipt.status == ReceiptWrite.REC_DSTN:
            raise ValueError()

        _status: str

        if action == "next":
            if receipt.status == ReceiptWrite.REC_ORGN:
                _status = ReceiptWrite.DPRT_ORGN
            if receipt.status == ReceiptWrite.DPRT_ORGN:
                _status = ReceiptWrite.ARVD_DSTN
            if receipt.status == ReceiptWrite.ARVD_DSTN:
                _status = ReceiptWrite.REC_DSTN

        if action == "prev":
            if receipt.status == ReceiptWrite.DPRT_ORGN:
                _status = ReceiptWrite.REC_ORGN
            if receipt.status == ReceiptWrite.ARVD_DSTN:
                _status = ReceiptWrite.DPRT_ORGN

        repr = RecordSerializer().to_representation(receipt)
        repr.pop("status")
        repr.pop("datetime")

        record = RecordSerializer(
            data={
                **repr,
                "status": _status,
                "datetime": None,
            }
        )
        record.is_valid(raise_exception=True)
        record.save()

        return response.Response(
            # [RecordSerializer().to_representation(receipt) for receipt in receipts],
            RecordSerializer().to_representation(record.instance),
            status=status.HTTP_200_OK,
        )

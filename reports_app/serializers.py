import datetime

from rest_framework import serializers

from reports_app.models import TransactionReport


class ReportRequestSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data: dict[str, datetime.date]) -> dict[str, datetime.date]:
        if data['end_date'] < data['start_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


class ReportResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionReport
        fields = '__all__'

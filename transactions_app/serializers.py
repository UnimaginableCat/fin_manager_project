from rest_framework import serializers

from transactions_app.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_amount(self, value: float) -> float:
        if value < 0:
            raise serializers.ValidationError("Amount must be non-negative.")
        return value

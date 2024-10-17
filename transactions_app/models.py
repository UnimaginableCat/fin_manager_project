import uuid
from django.db import models
from users_app.models import User

class TransactionType(models.TextChoices):
    INCOME = 'income', 'Income'
    EXPENSE = 'expense', 'Expense'

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionType.choices
    )
    category = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')

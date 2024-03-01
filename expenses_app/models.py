from django.db import models

SPLIT_METHOD_CHOICES = (
    ('EQUAL', 'Equal'),
    ('EXACT', 'Exact'),
    ('PERCENT', 'Percentage'),
)

class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name


class Expense(models.Model):
    paid_by_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    split_method = models.CharField(max_length=10, choices=SPLIT_METHOD_CHOICES)
    participants = models.ManyToManyField(User, related_name='expenses_involved')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expense of {self.total_amount} paid by {self.paid_by_user.username}"

class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='balances')
    owes = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owed_by')
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.name} owes {self.amount} to {self.owes.name}"

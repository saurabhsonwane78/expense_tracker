from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Loan(models.Model):
    description = models.CharField(max_length=300, null=True, blank=True)
    borrower = models.ForeignKey(User, related_name="loan_borrower", on_delete=models.CASCADE)
    lender = models.ForeignKey(User, related_name="loan_provider", on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=200, null=True, blank=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Refunds(models.Model):
    loan = models.ForeignKey(Loan, related_name='loan_refund', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(blank=True, null=True)
    payment_mode = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.loan} - {self.amount}"
    
class BorrowerBalance(models.Model):
    borrower = models.OneToOneField(User, on_delete=models.CASCADE)
    total_borrowed = models.IntegerField(default=0)
    total_refunded = models.IntegerField(default=0)
    total_outstanding = models.IntegerField(default=0)

    def update_totals(self):
        self.total_borrowed = Loan.objects.filter(borrower=self.borrower).aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_refunded = Refunds.objects.filter(loan__borrower=self.borrower).aggregate(Sum('amount'))['amount__sum'] or 0
        self.total_outstanding = self.total_borrowed - self.total_refunded
        self.save()

    def __str__(self):
        return f"{self.borrower.username} - Borrower Balance"
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Loan, Refunds, BorrowerBalance

@receiver(post_save, sender=Loan)
def update_borrower_balance_on_loan_save(sender, instance, **kwargs):
    borrower_balance, created = BorrowerBalance.objects.get_or_create(borrower=instance.borrower)
    borrower_balance.update_totals()

@receiver(post_save, sender=Refunds)
def update_borrower_balance_on_refund_save(sender, instance, **kwargs):
    borrower_balance, created = BorrowerBalance.objects.get_or_create(borrower=instance.loan.borrower)
    borrower_balance.update_totals()
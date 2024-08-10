from django.contrib import admin
from .models import Category, Loan, Refunds, BorrowerBalance
# Register your models here.
admin.site.register(Category)
admin.site.register(Loan)
admin.site.register(Refunds)
admin.site.register(BorrowerBalance)

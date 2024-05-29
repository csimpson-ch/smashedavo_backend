from django.contrib import admin
from .models import *

admin.site.register(BlogPost)
admin.site.register(Loan)
admin.site.register(ExpenseInterval)
admin.site.register(ExpenseAdhoc)

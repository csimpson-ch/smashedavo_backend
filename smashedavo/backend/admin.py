from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(BlogPost)
admin.site.register(Loan)
admin.site.register(RegularPayment)
admin.site.register(Expense)

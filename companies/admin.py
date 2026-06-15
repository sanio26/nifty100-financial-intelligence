from django.contrib import admin
from .models import *

admin.site.register(DimCompany)
admin.site.register(FactProfitLoss)
admin.site.register(FactBalanceSheet)
admin.site.register(FactCashFlow)
admin.site.register(FactAnalysis)
admin.site.register(FactMlScores)
admin.site.register(FactProsCons)
admin.site.register(FactDocuments)
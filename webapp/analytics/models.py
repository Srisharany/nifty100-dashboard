from django.db import models


class Company(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    company_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'companies'
        managed = False


class ProfitLoss(models.Model):
    company_id = models.CharField(max_length=20)
    year = models.CharField(max_length=50)
    sales = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    net_profit = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    eps = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_profit_loss'
        managed = False


class BalanceSheet(models.Model):
    company_id = models.CharField(max_length=20)
    year = models.CharField(max_length=50)
    total_assets = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    borrowings = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_balance_sheet'
        managed = False


class CashFlow(models.Model):
    company_id = models.CharField(max_length=20)
    year = models.CharField(max_length=50)
    operating_activity = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    class Meta:
        db_table = 'fact_cash_flow'
        managed = False


class Analysis(models.Model):
    company_id = models.CharField(max_length=20)
    roe = models.TextField(null=True)

    class Meta:
        db_table = 'fact_analysis'
        managed = False
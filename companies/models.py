# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DimCompany(models.Model):
    symbol = models.CharField(primary_key=True, max_length=20)
    company_name = models.TextField(blank=True, null=True)
    company_logo = models.TextField(blank=True, null=True)
    website = models.TextField(blank=True, null=True)
    nse_url = models.TextField(blank=True, null=True)
    bse_url = models.TextField(blank=True, null=True)
    face_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    book_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    roce_percentage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    roe_percentage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    about_company = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_company'


class DimYear(models.Model):
    year_id = models.AutoField(primary_key=True)
    year_label = models.CharField(unique=True, max_length=20, blank=True, null=True)
    fiscal_year = models.IntegerField(blank=True, null=True)
    is_ttm = models.BooleanField(blank=True, null=True)
    sort_order = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dim_year'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FactAnalysis(models.Model):
    company_id = models.CharField(max_length=20, blank=True, null=True)
    compounded_sales_growth = models.TextField(blank=True, null=True)
    compounded_profit_growth = models.TextField(blank=True, null=True)
    stock_price_cagr = models.TextField(blank=True, null=True)
    roe = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_analysis'


class FactBalanceSheet(models.Model):
    symbol = models.ForeignKey(DimCompany, models.DO_NOTHING, db_column='symbol', blank=True, null=True)
    year_label = models.CharField(max_length=20, blank=True, null=True)
    equity_capital = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    reserves = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    borrowings = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    other_liabilities = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_liabilities = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    fixed_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cwip = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    other_asset = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    total_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    debt_to_equity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    equity_ratio = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_balance_sheet'


class FactCashFlow(models.Model):
    symbol = models.ForeignKey(DimCompany, models.DO_NOTHING, db_column='symbol', blank=True, null=True)
    year_label = models.CharField(max_length=20, blank=True, null=True)
    operating_activity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    investing_activity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    financing_activity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    net_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    free_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_cash_flow'


class FactDocuments(models.Model):
    company_id = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)
    annual_report = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_documents'


class FactMlScores(models.Model):
    symbol = models.TextField(primary_key=True)
    company_name = models.TextField(blank=True, null=True)
    overall_score = models.FloatField(blank=True, null=True)
    health_label = models.TextField(blank=True, null=True)
    computed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_ml_scores'


class FactProfitLoss(models.Model):
    symbol = models.ForeignKey(DimCompany, models.DO_NOTHING, db_column='symbol', blank=True, null=True)
    year_label = models.CharField(max_length=20, blank=True, null=True)
    sales = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    expenses = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    operating_profit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    opm_percentage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    other_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    interest = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    depreciation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    profit_before_tax = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    tax_percentage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    net_profit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    eps = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    dividend_payout = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    net_profit_margin_pct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    expense_ratio_pct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    interest_coverage = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_profit_loss'


class FactProsCons(models.Model):
    company_id = models.CharField(max_length=20, blank=True, null=True)
    pros = models.TextField(blank=True, null=True)
    cons = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fact_pros_cons'

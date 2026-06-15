
from rest_framework import serializers
from .models import (
    DimCompany,
    FactMlScores,
    FactProfitLoss
)


# ===================================
# COMPANY SERIALIZER
# ===================================

class CompanySerializer(
    serializers.ModelSerializer
):

    roe_percentage =serializers.SerializerMethodField()

    roce_percentage =serializers.SerializerMethodField()


    class Meta:

        model = DimCompany

        fields = [

            "symbol",
            "company_name",
            "roe_percentage",
            "roce_percentage",
            "website",
        ]


    def get_roe_percentage(
        self,
        obj
    ):

        try:
            return float(
                obj.roe_percentage
            )

        except:
            return None


    def get_roce_percentage(
        self,
        obj
    ):

        try:
            return float(
                obj.roce_percentage
            )

        except:
            return None



# ===================================
# ML HEALTH SERIALIZER
# ===================================

class CompanyHealthSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = FactMlScores

        fields = [

            "symbol",
            "company_name",
            "overall_score",
            "health_label",
            "computed_at",
        ]




# ===================================
# PROFIT LOSS SERIALIZER
# ===================================

class ProfitLossSerializer(
    serializers.ModelSerializer
):

    sales = serializers.SerializerMethodField()

    operating_profit = (
        serializers.SerializerMethodField()
    )

    net_profit = (
        serializers.SerializerMethodField()
    )

    eps = (
        serializers.SerializerMethodField()
    )


    class Meta:

        model = FactProfitLoss

        fields = [

            "year_label",
            "sales",
            "operating_profit",
            "net_profit",
            "eps",
        ]


    def get_sales(
        self,
        obj
    ):

        try:
            return float(obj.sales)

        except:
            return None


    def get_operating_profit(
        self,
        obj
    ):

        try:
            return float(
                obj.operating_profit
            )

        except:
            return None


    def get_net_profit(
        self,
        obj
    ):

        try:
            return float(
                obj.net_profit
            )

        except:
            return None


    def get_eps(
        self,
        obj
    ):

        try:
            return float(obj.eps)

        except:
            return None

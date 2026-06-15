
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (
    CompanySerializer,
    CompanyHealthSerializer,
    ProfitLossSerializer
)


from django.shortcuts import render
from .models import (
    DimCompany,
    FactProfitLoss,
    FactMlScores,
    FactProsCons,
    FactDocuments
)

import json



def home(request):

    search_query = request.GET.get(
        "search",
        ""
    )

    companies = (
        DimCompany.objects.all()
    )

    if search_query:

        companies = (
            companies.filter(
                company_name__icontains=
                search_query
            )
        )

    context = {

        "companies":
            companies,

        "search_query":
            search_query,
    }

    return render(

        request,

        "companies/home.html",

        context
    )

def company_detail(request, symbol):

    company = DimCompany.objects.get(
        symbol=symbol
    )

    profit_data = (
        FactProfitLoss.objects
        .filter(symbol=symbol)
        .order_by("year_label")
    )

    ml_score = (
        FactMlScores.objects
        .filter(symbol=symbol)
        .first()
    )

    pros = (
        FactProsCons.objects
        .filter(
            company_id=symbol,
            pros__isnull=False
        )
    )

    cons = (
        FactProsCons.objects
        .filter(
            company_id=symbol,
            cons__isnull=False
        )
    )

    documents = (
        FactDocuments.objects
        .filter(company_id=symbol)
        .order_by("-year")
    )

    # ==========================
    # CHART DATA
    # ==========================

    sales_years = []
    sales_values = []

    profit_years = []
    profit_values = []

    for item in profit_data:

        sales_years.append(
            str(item.year_label)
        )

        sales_values.append(
            float(item.sales or 0)
        )

        profit_years.append(
            str(item.year_label)
        )

        profit_values.append(
            float(item.net_profit or 0)
        )

    context = {

        "company": company,

        "profit_data": profit_data,

        "ml_score": ml_score,

        "pros": pros,

        "cons": cons,

        "documents": documents,

        "sales_years":
            json.dumps(sales_years),

        "sales_values":
            json.dumps(sales_values),

        "profit_years":
            json.dumps(profit_years),

        "profit_values":
            json.dumps(profit_values),
    }

    return render(
        request,
        "companies/company_detail.html",
        context
    )

# ====================================
# API 1 — ALL COMPANIES
# ====================================

@api_view(["GET"])
def companies_api(request):

    companies = (
        DimCompany.objects.all()
    )

    serializer = CompanySerializer(
        companies,
        many=True
    )

    return Response(
        serializer.data
    )


# ====================================
# API 2 — SINGLE COMPANY
# ====================================

@api_view(["GET"])
def company_api(
    request,
    symbol
):

    company = (
        DimCompany.objects
        .filter(symbol=symbol)
        .first()
    )

    health = (
        FactMlScores.objects
        .filter(symbol=symbol)
        .first()
    )

    company_data = (
        CompanySerializer(company)
        .data
    )

    health_data = {}

    if health:

        health_data = (
            CompanyHealthSerializer(
                health
            ).data
        )

    response = {

        "company":
            company_data,

        "health":
            health_data,
    }

    return Response(response)


# ====================================
# API 3 — PROFIT LOSS
# ====================================

@api_view(["GET"])
def profit_loss_api(
    request,
    symbol
):

    profit_data = (

        FactProfitLoss.objects

        .filter(
            symbol=symbol
        )

        .order_by(
            "year_label"
        )
    )

    serializer = (
        ProfitLossSerializer(
            profit_data,
            many=True
        )
    )

    return Response(
        serializer.data
    )

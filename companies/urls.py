
from django.urls import path

from . import views


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "company/<str:symbol>/",
        views.company_detail,
        name="company_detail"
    ),

    # API URLs

    path(
        "api/companies/",
        views.companies_api
    ),

    path(
        "api/company/<str:symbol>/",
        views.company_api
    ),

    path(
        "api/profit-loss/<str:symbol>/",
        views.profit_loss_api
    ),
]

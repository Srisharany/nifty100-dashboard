from django.urls import path
from .views import (
    home,
    company_list,
    company_detail,
    CompanyAPI,
    ProfitLossAPI,
    BalanceSheetAPI,
    CashFlowAPI
)

urlpatterns = [
    path('', home),
    path('companies/', company_list),
    path('company/<str:symbol>/', company_detail),

    path('api/companies/', CompanyAPI.as_view()),
    path('api/profit/<str:symbol>/', ProfitLossAPI.as_view()),
    path('api/balance/<str:symbol>/', BalanceSheetAPI.as_view()),
    path('api/cashflow/<str:symbol>/', CashFlowAPI.as_view()),
]